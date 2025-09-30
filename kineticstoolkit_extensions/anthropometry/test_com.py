import kineticstoolkit.lab as ktk
import numpy as np
import kineticstoolkit_extensions.anthropometry as am

markers = ktk.load(ktk.doc.download("anthropometrics_static.ktk.zip"))

# Show in a Player
viewpoint = {
    "zoom": 3.5,
    "azimuth": -2.356,
    "elevation": 0.384,
    "translation": (0.083, 0.184),
    "target": (-4.435, 0.726, 0.540, 1.0),
}

#: A link model to help ktk.kinematics visualization
LINKS = {
    "Pelvis": {
        "Links": [
            ["AnteriorSuperiorIliacSpineR", "AnteriorSuperiorIliacSpineL"],
            ["AnteriorSuperiorIliacSpineL", "PosteriorSuperiorIliacSpineL"],
            ["PosteriorSuperiorIliacSpineL", "PosteriorSuperiorIliacSpineR"],
            ["PosteriorSuperiorIliacSpineR", "AnteriorSuperiorIliacSpineR"],
            ["AnteriorSuperiorIliacSpineR", "HipJointCenterR"],
            ["PosteriorSuperiorIliacSpineR", "HipJointCenterR"],
            ["AnteriorSuperiorIliacSpineL", "HipJointCenterL"],
            ["PosteriorSuperiorIliacSpineL", "HipJointCenterL"],
            ["AnteriorSuperiorIliacSpineR", "PubicSymphysis"],
            ["AnteriorSuperiorIliacSpineL", "PubicSymphysis"],
            ["HipJointCenterR", "PubicSymphysis"],
            ["HipJointCenterL", "PubicSymphysis"],
            ["HipJointCenterL", "HipJointCenterR"],
        ],
        "Color": [0.25, 0.5, 0.25],
    },
    "Trunk": {
        "Links": [
            ["L5S1JointCenter", "C7T1JointCenter"],
            ["C7", "GlenohumeralJointCenterR"],
            ["C7", "GlenohumeralJointCenterL"],
            ["Suprasternale", "GlenohumeralJointCenterR"],
            ["Suprasternale", "GlenohumeralJointCenterL"],
            ["C7", "AcromionR"],
            ["C7", "AcromionL"],
            ["Suprasternale", "AcromionR"],
            ["Suprasternale", "AcromionL"],
            ["GlenohumeralJointCenterR", "AcromionR"],
            ["GlenohumeralJointCenterL", "AcromionL"],
        ],
        "Color": [0.5, 0.5, 0],
    },
    "HeadNeck": {
        "Links": [
            ["Sellion", "C7T1JointCenter"],
            ["HeadVertex", "C7T1JointCenter"],
            ["Sellion", "HeadVertex"],
        ],
        "Color": [0.5, 0.5, 0.25],
    },
    "UpperArms": {
        "Links": [
            ["GlenohumeralJointCenterR", "ElbowJointCenterR"],
            ["GlenohumeralJointCenterR", "LateralHumeralEpicondyleR"],
            ["GlenohumeralJointCenterR", "MedialHumeralEpicondyleR"],
            ["LateralHumeralEpicondyleR", "MedialHumeralEpicondyleR"],
            ["GlenohumeralJointCenterL", "ElbowJointCenterL"],
            ["GlenohumeralJointCenterL", "LateralHumeralEpicondyleL"],
            ["GlenohumeralJointCenterL", "MedialHumeralEpicondyleL"],
            ["LateralHumeralEpicondyleL", "MedialHumeralEpicondyleL"],
        ],
        "Color": [0.5, 0.25, 0],
    },
    "Forearms": {
        "Links": [
            ["ElbowJointCenterR", "WristJointCenterR"],
            ["RadialStyloidR", "LateralHumeralEpicondyleR"],
            ["UlnarStyloidR", "MedialHumeralEpicondyleR"],
            ["RadialStyloidR", "UlnarStyloidR"],
            ["ElbowJointCenterL", "WristJointCenterL"],
            ["RadialStyloidL", "LateralHumeralEpicondyleL"],
            ["UlnarStyloidL", "MedialHumeralEpicondyleL"],
            ["RadialStyloidL", "UlnarStyloidL"],
        ],
        "Color": [0.5, 0, 0],
    },
    "Hands": {
        "Links": [
            ["RadialStyloidR", "CarpalMetaHead2R"],
            ["UlnarStyloidR", "CarpalMetaHead5R"],
            ["CarpalMetaHead2R", "CarpalMetaHead5R"],
            ["RadialStyloidL", "CarpalMetaHead2L"],
            ["UlnarStyloidL", "CarpalMetaHead5L"],
            ["CarpalMetaHead2L", "CarpalMetaHead5L"],
        ],
        "Color": [0.5, 0, 0.25],
    },
    "Tighs": {
        "Links": [
            ["HipJointCenterR", "KneeJointCenterR"],
            ["HipJointCenterR", "LateralFemoralEpicondyleR"],
            ["HipJointCenterR", "MedialFemoralEpicondyleR"],
            ["LateralFemoralEpicondyleR", "MedialFemoralEpicondyleR"],
            ["HipJointCenterL", "KneeJointCenterL"],
            ["HipJointCenterL", "LateralFemoralEpicondyleL"],
            ["HipJointCenterL", "MedialFemoralEpicondyleL"],
            ["LateralFemoralEpicondyleL", "MedialFemoralEpicondyleL"],
        ],
        "Color": [0, 0.5, 0.5],
    },
    "Legs": {
        "Links": [
            ["AnkleJointCenterR", "KneeJointCenterR"],
            ["LateralMalleolusR", "LateralFemoralEpicondyleR"],
            ["MedialMalleolusR", "MedialFemoralEpicondyleR"],
            ["LateralMalleolusR", "MedialMalleolusR"],
            ["AnkleJointCenterL", "KneeJointCenterL"],
            ["LateralMalleolusL", "LateralFemoralEpicondyleL"],
            ["MedialMalleolusL", "MedialFemoralEpicondyleL"],
            ["LateralMalleolusL", "MedialMalleolusL"],
        ],
        "Color": [0, 0.25, 0.5],
    },
    "Feets": {
        "Links": [
            ["CalcaneusR", "TarsalMetaHead1R"],
            ["CalcaneusR", "TarsalMetaHead5R"],
            ["MedialMalleolusR", "TarsalMetaHead1R"],
            ["LateralMalleolusR", "TarsalMetaHead5R"],
            ["CalcaneusR", "MedialMalleolusR"],
            ["CalcaneusR", "LateralMalleolusR"],
            ["TarsalMetaHead1R", "TarsalMetaHead5R"],
            ["CalcaneusL", "TarsalMetaHead1L"],
            ["CalcaneusL", "TarsalMetaHead5L"],
            ["MedialMalleolusL", "TarsalMetaHead1L"],
            ["LateralMalleolusL", "TarsalMetaHead5L"],
            ["CalcaneusL", "MedialMalleolusL"],
            ["CalcaneusL", "LateralMalleolusL"],
            ["TarsalMetaHead1L", "TarsalMetaHead5L"],
        ],
        "Color": [0.25, 0.0, 0.75],
    },
}

# player = ktk.Player(
#     markers,
#     interconnections=LINKS,  # Lines to better see the human shape
#     **viewpoint
# )

# %% Infer joint centers

# Ankles
markers.data["AnkleJointCenterR"] = 0.5 * (
    markers.data["MedialMalleolusR"] + markers.data["LateralMalleolusR"]
)
markers.data["AnkleJointCenterR"] = 0.5 * (
    markers.data["MedialMalleolusR"] + markers.data["LateralMalleolusR"]
)

# Knees
markers.data["KneeJointCenterR"] = 0.5 * (
    markers.data["LateralFemoralEpicondyleR"]
    + markers.data["MedialFemoralEpicondyleR"]
)
markers.data["KneeJointCenterL"] = 0.5 * (
    markers.data["LateralFemoralEpicondyleL"]
    + markers.data["MedialFemoralEpicondyleL"]
)

# Hips
markers.data["HipJointCenterR"] = am.infer_hip_joint_center_reed1999(
    rasis=markers.data["AnteriorSuperiorIliacSpineR"],
    lasis=markers.data["AnteriorSuperiorIliacSpineL"],
    sym=markers.data["PubicSymphysis"],
    side="R",
    sex="M",
)
markers.data["HipJointCenterL"] = am.infer_hip_joint_center_reed1999(
    rasis=markers.data["AnteriorSuperiorIliacSpineR"],
    lasis=markers.data["AnteriorSuperiorIliacSpineL"],
    sym=markers.data["PubicSymphysis"],
    side="L",
    sex="M",
)

# L5S1
markers.data["L5S1JointCenter"] = am.infer_l5s1_joint_center_reed1999(
    rasis=markers.data["AnteriorSuperiorIliacSpineR"],
    lasis=markers.data["AnteriorSuperiorIliacSpineL"],
    sym=markers.data["PubicSymphysis"],
    sex="M",
)

# C7T1
markers.data["C7T1JointCenter"] = am.infer_c7t1_joint_center_dumas2018(
    c7=markers.data["C7"],
    l5s1=markers.data["L5S1JointCenter"],
    sup=markers.data["Suprasternale"],
    rac=markers.data["AcromionR"],
    lac=markers.data["AcromionL"],
    sex="M",
)

# Glenohumeral joints
markers.data["GlenohumeralJointCenterR"] = am.infer_gh_joint_center_rab2002(
    c7=markers.data["C7"],
    l5s1=markers.data["L5S1JointCenter"],
    sup=markers.data["Suprasternale"],
    rac=markers.data["AcromionR"],
    lac=markers.data["AcromionL"],
    sex="M",
    side="R",
)

markers.data["GlenohumeralJointCenterL"] = am.infer_gh_joint_center_rab2002(
    c7=markers.data["C7"],
    l5s1=markers.data["L5S1JointCenter"],
    sup=markers.data["Suprasternale"],
    rac=markers.data["AcromionR"],
    lac=markers.data["AcromionL"],
    sex="M",
    side="L",
)

# Elbows
markers.data["ElbowJointCenterR"] = 0.5 * (
    markers.data["MedialHumeralEpicondyleR"]
    + markers.data["LateralHumeralEpicondyleR"]
)
markers.data["ElbowJointCenterL"] = 0.5 * (
    markers.data["MedialHumeralEpicondyleL"]
    + markers.data["LateralHumeralEpicondyleL"]
)

# Wrists
markers.data["WristJointCenterR"] = 0.5 * (
    markers.data["UlnarStyloidR"]
    + markers.data["RadialStyloidR"]
)
markers.data["WristJointCenterL"] = 0.5 * (
    markers.data["UlnarStyloidL"]
    + markers.data["RadialStyloidL"]
)

player = ktk.Player(
    markers,
    interconnections=LINKS,  # Lines to better see the human shape
    **viewpoint
)

