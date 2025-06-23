#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Félix Chénier

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
Read NDI Optotrak N3D files.
"""

__author__ = "Félix Chénier"
__copyright__ = "Copyright (C) 2022 Félix Chénier"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"


from kineticstoolkit import TimeSeries
import struct
import numpy as np
from typing import Sequence


def read_n3d(filename: str, labels: Sequence[str] = []) -> TimeSeries:
    """
    Read markers from an NDI N3D file.

    The markers positions are returned in a TimeSeries where each marker
    corresponds to a data key. Each marker position is expressed in this form:

    array([[x0, y0, z0, 1.], [x1, y1, z1, 1.], [x2, y2, z2, 1.], ...])

    Parameters
    ----------
    filename : str
        Path of the N3D file.
    labels : list of str (optional)
        Marker names

    Returns
    -------
    TimeSeries

    """
    with open(filename, "rb") as fid:
        _ = fid.read(1)  # 32
        n_markers = struct.unpack("h", fid.read(2))[0]
        n_data_per_marker = struct.unpack("h", fid.read(2))[0]
        n_columns = n_markers * n_data_per_marker

        n_frames = struct.unpack("i", fid.read(4))[0]

        collection_frame_frequency = struct.unpack("f", fid.read(4))[0]
        user_comments = struct.unpack("60s", fid.read(60))[0]
        system_comments = struct.unpack("60s", fid.read(60))[0]
        file_description = struct.unpack("30s", fid.read(30))[0]
        cutoff_filter_frequency = struct.unpack("h", fid.read(2))[0]
        time_of_collection = struct.unpack("8s", fid.read(8))[0]
        _ = fid.read(2)
        date_of_collection = struct.unpack("8s", fid.read(8))[0]
        extended_header = struct.unpack("73s", fid.read(73))[0]

        # Read the rest and put it in an array
        ndi_array = np.ones((n_frames, n_columns)) * np.nan

        for i_frame in range(n_frames):
            for i_column in range(n_columns):
                data = struct.unpack("f", fid.read(4))[0]
                if data < -1e25:  # technically, it is -3.697314e+28
                    data = np.nan
                ndi_array[i_frame, i_column] = data

        # Conversion from mm to meters
        ndi_array /= 1000

        # Transformation to a TimeSeries
        ts = TimeSeries(
            time=np.linspace(
                0, n_frames / collection_frame_frequency, n_frames
            )
        )

        for i_marker in range(n_markers):
            if labels != []:
                label = labels[i_marker]
            else:
                label = f"Marker{i_marker}"

            ts.data[label] = np.block(
                [
                    [
                        ndi_array[:, 3 * i_marker : 3 * i_marker + 3],
                        np.ones((n_frames, 1)),
                    ]
                ]
            )
            ts = ts.add_data_info(label, "Unit", "m")

    return ts



if __name__ == "__main__":  # pragma: no cover
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
