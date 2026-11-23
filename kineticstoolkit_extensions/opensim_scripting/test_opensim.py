#!/usr/bin/env python3
#
# Copyright 2020-2025 Félix Chénier

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Unit tests, to be run using pytest."""

__author__ = "Félix Chénier"
__copyright__ = "Copyright (C) 2020-2025 Félix Chénier"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"


import math
import os
import sys
from pathlib import Path

import kineticstoolkit as ktk

from kineticstoolkit_extensions import opensim_scripting as opensim

this_folder = os.path.dirname(__file__)


# Find the python interpreter in the "opensim" conda environment, assuming
# we are already in a conda environment.
if ktk.config.is_pc:
    env_dir = os.path.dirname(sys.executable)
    opensim.configure(
        python_path=os.path.dirname(env_dir) + "\\opensim\\python.exe"
    )
else:
    env_dir = os.path.dirname(os.path.dirname(sys.executable))
    opensim.configure(
        python_path=os.path.dirname(env_dir) + "/opensim/bin/python"
    )


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])


def get_scale_factor(lines):
    """
    Detect the unit in the header of a .trc file.

    Return the factorin millimeters.
    """
    # In a .trc standard, the units ('m' or 'mm') are in the first 4 lines
    header_tokens = " ".join(lines[:4]).split()
    if "m" in header_tokens:
        return 1000.0
    return 1.0


def test_write__read_trc():
    """
    Test the write_trc and read_trc functions.

    Compare the two TRC files we have.

    """
    # Finding the folder where test_opensim.py is located
    root_folder = Path(__file__).parent
    name_marker_trc = "subject01_static.trc"
    path_folder = (root_folder / "data" / name_marker_trc).as_posix()
    ts = opensim.read_trc(path_folder)
    output_path = root_folder / "new_file.trc"
    opensim.write_trc(output_path.as_posix(), ts)

    # Comparison of the two trc files
    with (
        open(path_folder, encoding="utf-8") as f1,
        open(output_path, encoding="utf-8") as f2,
    ):
        input_trc = f1.readlines()[1:]
        output_trc = f2.readlines()[1:]

    # We bring back the two files in millimeters.
    scale1 = get_scale_factor(input_trc)
    scale2 = get_scale_factor(output_trc)

    if len(input_trc) != len(output_trc):
        pytest.fail(
            f"Different number of rows :\n"
            f" input : {len(input_trc)} rows\n"
            f" output : {len(output_trc)} rows"
        )

    for row_num, (trc_in, trc_out) in enumerate(
        zip(input_trc, output_trc, strict=True), start=2
    ):
        tokens_in = trc_in.split()
        tokens_out = trc_out.split()

        for col_num, (i, j) in enumerate(
            zip(tokens_in, tokens_out, strict=True), start=1
        ):
            try:
                # If these are numbers, we compare with tolerance
                v1, v2 = float(i), float(j)
                if math.isnan(v1) and math.isnan(v2):
                    continue
                # These are the X, Y, Z coordinates.
                if row_num >= 7 and col_num >= 3:
                    v1 *= scale1
                    v2 *= scale2

                if not math.isclose(v1, v2, rel_tol=1e-4, abs_tol=1e-2):
                    pytest.fail(
                        f"Numeric difference at row {row_num}, column {col_num} :\n"
                        f"  input (en mm) : {v1}\n"
                        f"  output  (en mm) : {v2}\n"
                    )
            except ValueError:
                # If it is text, exact equality is required
                # Exception for units if it's m versus mm
                if row_num == 3 and {i, j} == {"mm", "m"}:
                    continue

                if i != j:
                    pytest.fail(
                        f"Text difference at {row_num}, {col_num} column:\n"
                        f"  input : '{i}'\n"
                        f"  output  : '{j}'"
                    )


def test_scaling():
    """
    Test the run_scaling function.

    Compare the osim folder.

    """
    # Finding the folder where test_opensim.py is located
    root_folder = Path(__file__).parent

    # List of all the necessary files

    name_model = "gait2354_simbody.osim"
    name_reference_xml = "subject01_Setup_Scale.xml"
    name_marker_xml = "gait2354_Scale_MarkerSet.xml"
    name_marker_trc = "subject01_static.trc"
    datas = [name_model, name_reference_xml, name_marker_xml, name_marker_trc]

    # Path to the files in the 'data' folder
    path_data = []
    for i in datas:
        path_folder = root_folder / "data" / i
        path_data.append(path_folder.as_posix())

    # Transformation of the trc into TimeSeries
    ts = opensim.read_trc(path_data[-1])
    mass = 72.60

    # Testing the run_scaling function
    final_result = opensim.run_scaling(
        path_data[0], path_data[1], path_data[2], ts, mass
    )
    assert final_result is not None
