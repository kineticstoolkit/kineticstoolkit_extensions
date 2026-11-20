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


import os
import sys
from pathlib import Path
import kineticstoolkit as ktk
from kineticstoolkit_extensions import opensim_scripting as opensim
from kineticstoolkit_extensions.opensim_scripting import run_scaling, write_trc, read_trc


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




def test_write_trc():
    # Finding the folder where test_opensim.py is located
    root_folder = Path(__file__).parent
    name_marker_trc = "subject01_static.trc"
    path_folder = (root_folder/"data"/name_marker_trc).as_posix()
    ts = read_trc(path_folder)
    output_path = (root_folder / "new_file.trc")
    write_trc(output_path.as_posix(), ts)
    assert output_path.exists()


def test_scaling() :
    """
    WARNING : Define the configuration in the __init__ file

    """

    # Finding the folder where test_opensim.py is located
    root_folder = Path(__file__).parent

    # List of all the necessary files

    name_model = "gait2354_simbody.osim"
    name_reference_xml = "subject01_Setup_Scale.xml"
    name_marker_xml = "gait2354_Scale_MarkerSet.xml"
    name_marker_trc = "subject01_static.trc"
    datas = [name_model,name_reference_xml,name_marker_xml,name_marker_trc]

    # Path to the files in the 'data' folder
    path_data = []
    for i in datas:
        path_folder = root_folder/"data"/i
        path_data.append(path_folder.as_posix())

    # Transformation of the trc into TimeSeries
    ts = read_trc(path_data[-1])
    mass = 72.60

    # Testing the run_scaling function
    final_result = run_scaling(path_data[0], path_data[1], path_data[2], ts, mass)
    assert final_result is not None





if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
