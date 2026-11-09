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
import warnings
import subprocess
import numpy as np
import pandas as pd
from pathlib import Path
import kineticstoolkit as ktk
from kineticstoolkit_extensions import opensim_scripting as opensim
from __init__ import run_scaling


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
    """TODO."""
    pass


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])

def test_scaling() :
    
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