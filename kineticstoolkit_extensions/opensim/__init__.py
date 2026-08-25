#!/usr/bin/env python3
#
# Copyright 2026 Mobility and Adaptive System Research Lab

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Provide support for analysing movement data using OpenSim.
"""

__author__ = "Mobility and Adaptive System Research Lab"
__copyright__ = "Copyright (C) 2026 Mobility and Adaptive System Research Lab"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"


import subprocess

from kineticstoolkit import TimeSeries


class Config:
    """Module configuration."""

    python_path: str = ""


config = Config()


def configure(python_path: str = "") -> None:
    """
    Configure the extension.

    Parameters
    ----------
    python_path
        Path of the python instance opensim is installed in.

    """
    config.python_path = python_path


def run_scaling() -> None:
    """
    Run a scaling operation.

    !TODO Determine arguments and return value.

    This function will take its input and create the required TRC from it,
    then launch a process that runs "run_scaling.py", and finally open the
    results, process it and return it.

    """
    # TODO Do something from the arguments
    print(
        subprocess.check_output(
            [config.python_path, "run_scaling.py"]
        ).decode()
    )
    # TODO Do something and return it


def write_trc(filename: str, points: TimeSeries) -> None:
    """
    Export a TimeSeries or points to OpenSim's TRC file format.

    Parameters
    ----------
    points
        Points trajectories.

    filename
        Name of the trc file to create.

    Caution
    -------
    OpenSim expects no missing markers, and therefore it could be a good idea
    to use points.fill_missing_samples before using write_trc.

    """
    points = points.copy()

    n_points = len(points.data)
    n_frames = points.time.shape[0]
    data_rate = points.get_sample_rate()
    camera_rate = points.get_sample_rate()
    units = "m"

    # Open file
    with open(filename, "w") as fid:
        fid.write(f"PathFileType\t4\t(X/Y/Z)\t{filename}\n")
        fid.write(
            "DataRate\tCameraRate\tNumFrames\tNumMarkers\tUnits\t"
            "OrigDataRate\tOrigDataStartFrame\tOrigNumFrames\n"
        )
        fid.write(
            f"{data_rate}\t{camera_rate}\t{n_frames}\t{n_points}\t"
            f"{units}\t{data_rate}\t1\t{n_frames}\n"
        )

        # Write marker names
        fid.write("Frame#\tTime")
        fid.writelines(f"\t{key}\t\t" for key in points.data)
        fid.write("\n")

        # Write coordinate names
        fid.write("\t")
        fid.writelines(
            f"\tX{i + 1}\tY{i + 1}\tZ{i + 1}"
            for i, key in enumerate(points.data)
        )
        fid.write("\n\n")

        # Write trajectories
        for i_frame in range(n_frames):
            fid.write(f"{i_frame + 1}\t{{:.3f}}".format(points.time[i_frame]))
            fid.writelines(
                f"\t{points.data[key][i_frame, 0]:.5f}"
                + f"\t{points.data[key][i_frame, 1]:.5f}"
                + f"\t{points.data[key][i_frame, 2]:.5f}"
                for key in points.data
            )
            fid.write("\n")


if __name__ == "__main__":  # pragma: no cover
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
