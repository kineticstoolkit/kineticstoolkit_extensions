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
args = {"model_input" : "C:/Users/domit/Documents/Domitille/test/CaptureTestFinal.osim",
"scale_input" : "C:/Users/domit/Documents/Domitille/test/Scale_Settings_test.xml",
"marker_xml" : "C:/Users/domit/Documents/Domitille/test/CaptureTestmarkers.xml",
"marker_trc": "C:/Users/domit/Documents/Domitille/test/n_pose_001_1.trc",
"mass" : 80,
"folder_output" : "C:/Users/domit/OneDrive - Fondation EPF/4A"}
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
# setApply sert à replacer les marqueurs après la mise à l'échelle des os
marker_placer.setApply(True)
marker_placer.setMarkerFileName(args["marker_trc"])
marker_placer.setOutputModelFileName(model_output)

# Ecriture des modifications faites avant dans le XML
scale_tool.printToXML(scale)

if not scale_tool.run():
        raise RuntimeError("Scaling failed, check opensim.log")
else :
    print("scale successfull execute")
scaled_model = osim.Model(model_output)
scaled_model.initSystem()
print(scaled_model)

# Ajout de nouvelles valeurs dans le dictionnaire
args["model_output"] = model_output
args["scale_output"] = dest

#Ecriture fichier json
with open("args.json", "w", encoding="utf-8") as file:
    json.dump(args, file, indent=4, ensure_ascii=False)
print("Données sauvegardées avec succès !")

# Copie du fichier Json et enregistrement dans le dossier de sortie
path_json = Path(script_dir / "args.json")
shutil.copy("args.json", path_json)

#!TODO Write the code for a scaling operation
print("I've been run. !TODO Remove this call at some point.")









