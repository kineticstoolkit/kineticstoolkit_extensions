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
import warnings
import pandas as pd
import numpy as np
import kineticstoolkit.lab as ktk
from kineticstoolkit import TimeSeries
import json
from pathlib import Path



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


configure() # Enter the path to your OpenSim environment


def run_scaling(model : str, reference_xml : str, marker_xml : str, marker_ts : ktk.TimeSeries , mass : float , folder_output : str = None) -> dict:
    """
    Run a scaling operation.

    Caution
    -------
    Please, make sure you have an existing Opensim environment on your computer
    Define the configuration in the before run the function
    Remember that your entries are in the format: r"C:\..."

    Parameters
    ----------
    model
        Path of the osim model on which the scaling will be based

    reference_xml
        Path of the xml file that will be used to create a scaled xml file

    marker_xml
       Path of the xml file containing the positions of the markers on the rigid bodies

    marker_ts
        TimeSeries containing the names and positions of markers at a static moment.
        Make sure you have a clean TimeSeries before launching the function

    mass
        mass that we want for our scaled model

    folder_output
        where you want to save new files


    Returns
    -------
    arg
        Dictionary composed of the access paths of all the files necessary for this
        function and created during it

    """
    # Definition of the exit folder if it was not given as an input
    if folder_output is None:
        folder_output = Path.cwd().as_posix()


    # Creation of a TRC file based on the TimeSerie
    output_dir = Path(folder_output)
    output_file = (output_dir/"marker_trc.trc").as_posix()
    write_trc(output_file, marker_ts)
    chemin_trc = Path(output_file).resolve().as_posix()

    # Json file creation
    # Here, we use Path to homogenize the structures of access paths
    args = {
        "model_input" : Path(model).resolve().as_posix(),
        "scale_input" : Path(reference_xml).resolve().as_posix(),
        "marker_xml" : Path(marker_xml).resolve().as_posix(),
        "marker_trc" : chemin_trc,
        "mass" : mass,
        "folder_output" : Path(folder_output).resolve().as_posix(),
        }


    with open("args.json", "w", encoding="utf-8") as file:
        json.dump(args, file, indent=4, ensure_ascii=False)

    print(
        subprocess.check_output(
            [config.python_path, "run_scaling.py"]
        ).decode()
    )

    # Loading the modified json file
    with open("args.json", "r", encoding="utf-8") as file:
        args = json.load(file)

    return args


def read_trc(filename: str) -> ktk.TimeSeries:
    """
    Import an OpenSim TRC file and convert it to a TimeSeries.

    Parameters
    ----------
    filename
        Path of the file trc

    Returns
    ----------
    ts
        TimeSeries from the starting trc file

    """
    # Reading the 3rd line (1-2nd lines not necessary to build a TimeSeries)
    header_meta = pd.read_csv(filename, sep="\t", skiprows=2, nrows=1, header=None)
    # Recovery values from Data_rate and Camera_rate
    data_rate = float(header_meta.iloc[0, 2])
    camera_rate = float(header_meta.iloc[0, 1])

    units = str(header_meta.iloc[0, 4]) if header_meta.shape[1] > 4 else "m"
    scale = 0.001 if units.lower() == "mm" else 1.0
    if units.lower() == "mm":
        units = "m"

    # Reading the 4th line
    raw_markers = pd.read_csv(filename, sep="\t", skiprows=3, nrows=1, header=None)

    # Creating a list of marker names by removing unnecessary spaces
    marker_names = [str(col).strip() for col in raw_markers.iloc[0, 2:].dropna() if str(col).strip()]

    # skiprows=6 skips the first 6 lines to get the raw data
    df = pd.read_csv(filename, sep=r"\s+", skiprows=6, header=None)

    # We filter to keep only the digital lines
    #errors = "coerce" transforms untransformed character strings into numbers, in NAN

    df = df.apply(pd.to_numeric, errors="coerce")

    # Time Recovery (2nd column of the DataFrame)
    time = df.iloc[:, 1].to_numpy()
    n_frames = len(time)  #nb de frame

    # Reconstruction of the 4D dictionary for KTK
    data = {}
    col_idx = 2  # The coordinates begin at column 3 (index 2)

    for key in marker_names:
        # Extract the 3 columns X, Y, Z as a NumPy matrix, for a future time series
        xyz = df.iloc[:, col_idx : col_idx + 3].to_numpy() * scale

        # Create the matrix (n_frames, 4) with the 4th column at 1.0
        data_4d = np.ones((n_frames, 4))
        data_4d[:, :3] = xyz
        data[key] = data_4d

        col_idx += 3 #transition to the next marker’s coordinates

    # Recovery of the informations
    info = {"Time": {"Unit": "s"},
            "Header": {"DataRate": str(data_rate),
            "Camera_rate" : str(camera_rate)}}

    for key in marker_names:
        info[key] = {"Unit": units}

    ts = ktk.TimeSeries(data=data, time=time, info=info)

    # We check that the data recording is regular; if it is not, we manually calculate the time of the timeout.
    warnings.warn("If your TimeSerie data is not calculated at regular intervals, it is mandatory to manually calculate the time for a sample")

    if np.isnan(ts.get_sample_rate()):
        start = time[0]
        stop = time[-1]
        n_sample = len(time)
        ts.time = np.linspace(start, stop,n_sample)

    return ts


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
