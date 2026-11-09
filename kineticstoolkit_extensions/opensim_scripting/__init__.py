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



def run_scaling(model : str, reference_xml : str, marker_xml : str, marker_ts : ktk.TimeSeries , mass : float , other_env : str, folder_output : str = None) -> dict:
    """
    Run a scaling operation.
    
    Caution
    -------
    Please, make sure you have an existing Opensim environment on your computer
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
    
    other_env
        Opensim environment access path
        
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

    # Recovery the run_scaling.py path
    root_folder = Path.cwd()
    path_folder = (root_folder/"run_scaling.py").as_posix()
    
    # Create a osim model and return it
    # Launch of run_scaling.py
    output = subprocess.check_output(
        [other_env, path_folder],
        text=True  
        )
    print(output)
    
    # Loading the modified json file
    with open("args.json", "r", encoding="utf-8") as file:
        args = json.load(file)
    
    return args


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
