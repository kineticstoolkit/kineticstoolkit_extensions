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


"""Run a scale operation in OpenSim."""

__author__ = "Mobility and Adaptive System Research Lab"
__copyright__ = "Copyright (C) 2026 Mobility and Adaptive System Research Lab"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"

import opensim as osim
import json
import shutil
from pathlib import Path



"""
Example of our ARGS file : 
    args = {"model_input" : "C:/Users/model.osim",
            "scale_input" : "C:/Users/scale.xml",
            "marker_xml" : "C:/Users/markers.xml",
            "marker_trc": "C:/Users/marker.trc",
            "mass" : 80,
            "folder_output" : "C:/Users/output"}
"""


# Loading data from json file
with open("args.json", "r", encoding="utf-8") as file:
    args = json.load(file)
print(args)




# Creating model scaled
script_dir = Path(args["folder_output"])
model_output = (script_dir / "Model_Output.osim").as_posix()

# Creating scale xml copy
dest = Path(script_dir/ "Scale_Output.xml").as_posix()
scale = shutil.copy(args["scale_input"], dest)

 

# Upload XML scaling
scale_tool = osim.ScaleTool(scale)
#Avoid path conflicts
scale_tool.setPathToSubject("")

scale_tool.setSubjectMass(args["mass"])

generic_model_maker = scale_tool.getGenericModelMaker()
generic_model_maker.setModelFileName(args["model_input"])
generic_model_maker.setMarkerSetFileName(args["marker_xml"])

model_scaler = scale_tool.getModelScaler()
model_scaler.setApply(True)
model_scaler.setMarkerFileName(args["marker_trc"])

marker_placer = scale_tool.getMarkerPlacer()
# setApply is used to replace the markers after scaling bones
marker_placer.setApply(True)
marker_placer.setMarkerFileName(args["marker_trc"])
marker_placer.setOutputModelFileName(model_output)

# Writing the changes just made before in the XML
scale_tool.printToXML(scale)

if not scale_tool.run():
        raise RuntimeError("Scaling failed, check opensim.log")
else :
    print("scale successfull execute")
scaled_model = osim.Model(model_output)
scaled_model.initSystem()
print(scaled_model)

# Adding new values to the dictionary
args["model_output"] = model_output
args["scale_output"] = dest

#Writing JSON file
with open("args.json", "w", encoding="utf-8") as file:
    json.dump(args, file, indent=4, ensure_ascii=False)
print("Données sauvegardées avec succès !")

# Copy the JSON file and save it in the output folder if the output file is different from the current folder
path_json = Path(script_dir / "args.json")
if Path("args.json").resolve() != path_json : 
    shutil.copy("args.json", path_json)










