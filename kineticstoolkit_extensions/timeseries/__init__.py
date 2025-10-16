#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

"""
Provides additional generic TimeSeries utilities.
"""

__author__ = "Félix Chénier"
__copyright__ = "Copyright (C) 2025 Félix Chénier"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"


import kineticstoolkit as ktk
from kineticstoolkit.typing_ import ArrayLike, check_param
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageGrab  # to import from clipboard


def __dir__():
    return [
        "ui_draw",
    ]


def ui_draw(
    filename: str | None = None,
    *,
    time_range: ArrayLike | None = None,
    value_range: ArrayLike | None = None,
    data_keys: str | list[str] = "data",
    data_units: str | list[str] | None = None,
) -> ktk.TimeSeries:
    """
    Create a TimeSeries by letting the user draw the curve on a picture.

    Parameters
    ----------
    filename
        Optional. The image file to load. If not provided, the clipboard
        content is loaded instead.
    time_range
        Optional. Used to calibrate the time attribute. For example, if the
        time axis has visible ticks for 0.0 and 2.0 seconds, then
        use time_range = [0., 2.], and click on these ticks when requested.
        If time_range is not defined, a range of [0., 1.] is used, based on
        the minimal and maximal time.
    value_range
        Optional. Used to calibrate the y-axis. For example, if the y-axis
        has visible ticks for -100 newton and +200 newton, then use
        value+range = [-100., 200.], and click on these ticks when requested.
        If value_range is not defined, a range of [0., 1.] is used, based on
        the minimal and maximal values.
    data_keys
        Optional. For only one curve, the name of the data key in the resulting
        TimeSeries. Default is "data". For many curves, a list of data keys.
    data_units
        Optional. The units, which is returned in data TimeSeries' info
        attribute. If can be either a string, in which case the same unit is
        copied for each curves, or a list of strings of the same length as
        data_keys.

    Returns
    -------
    ktk.TimeSeries
        A TimeSeries with one data that corresponds to the draw points, one
        point per user's click.

    """
    # Check parameters
    if filename is not None:
        check_param("filename", filename, str)
    if time_range is not None:
        time_range = np.array(time_range)
    if value_range is not None:
        value_range = np.array(value_range)

    if isinstance(data_keys, str):
        data_keys = [data_keys]
    check_param("data_keys", data_keys, list, contents_type=str)

    if isinstance(data_units, str):
        data_units = [data_units for _ in data_keys]
    if data_units is not None:
        check_param("data_units", data_units, list, contents_type=str)

    # Load the image
    if filename is None:
        try:
            img = ImageGrab.grabclipboard()
        except TypeError:
            raise TypeError("The clipboard does not contain an image.")
    else:
        img = Image.open(filename)

    # For default time_range and value_range
    min_time_in_pixels = np.inf
    max_time_in_pixels = -np.inf
    min_value_in_pixels = np.inf
    max_value_in_pixels = -np.inf

    # Plot the image
    fig = plt.figure()
    plt.imshow(img)
    plt.xticks([])
    plt.yticks([])

    # Draw the curves
    time_in_pixels_dict = {}
    value_in_pixels_dict = {}

    for data_key in data_keys:

        plt.title(
            f"Draw the curved named {data_key} using multiple left-clicks, \n"
            "Remove last point using right-click or DELETE, \n"
            "Terminate using middle-click or ENTER.",
        )
        plt.tight_layout()
        plt.draw()

        # Get points
        point_array = np.array(plt.ginput(-1, timeout=0))

        # Sort and extract points
        sorted_index = point_array[:, 0].argsort()

        time_in_pixels_dict[data_key] = point_array[sorted_index, 0]
        value_in_pixels_dict[data_key] = -point_array[
            sorted_index, 1
        ]  # Inverted because it's a picture

        # For default time_range and value_range
        min_time_in_pixels = min(
            min_time_in_pixels, min(time_in_pixels_dict[data_key])
        )
        max_time_in_pixels = max(
            max_time_in_pixels, max(time_in_pixels_dict[data_key])
        )
        min_value_in_pixels = min(
            min_value_in_pixels, min(value_in_pixels_dict[data_key])
        )
        max_value_in_pixels = max(
            max_value_in_pixels, max(value_in_pixels_dict[data_key])
        )

    # Get time range
    if time_range is not None:
        plt.title(
            "Click on the time axis at \n"
            f"t={time_range[0]}, then t={time_range[1]}",
        )
        plt.draw()
        time_range_in_pixels = np.array(plt.ginput(2, timeout=0))[:, 0]
        time_range_in_pixels.sort()
    else:
        time_range_in_pixels = [min_time_in_pixels, max_time_in_pixels]

    # Get value range
    if value_range is not None:
        plt.title(
            "Click on the vertical axis at \n"
            f"y={value_range[0]}, then y={value_range[1]}",
        )
        plt.draw()
        value_range_in_pixels = -np.array(plt.ginput(2, timeout=0))[
            :, 1
        ]  # Inverted because it's a picture
        value_range_in_pixels.sort()
    else:
        value_range_in_pixels = [min_value_in_pixels, max_value_in_pixels]

    plt.close(fig)

    # Construct the output TimeSeries and scale values (not time yet)
    new_time = set()
    for key in time_in_pixels_dict:
        new_time = new_time.union(set(time_in_pixels_dict[key]))

    out_ts = ktk.TimeSeries(time=sorted(list(new_time)))

    for i_key, key in enumerate(value_in_pixels_dict):
        time_in_pixels = time_in_pixels_dict[key]
        value_in_pixels = value_in_pixels_dict[key]

        # Scale values
        value = (value_in_pixels - value_range_in_pixels[0]) * (
            value_range[1] - value_range[0]
        ) / (
            value_range_in_pixels[1] - value_range_in_pixels[0]
        ) + value_range[
            0
        ]

        # Add the unit
        temp_ts = ktk.TimeSeries(time=time_in_pixels, data={key: value})
        if data_units is not None:
            temp_ts.add_info(key, "Unit", data_units[i_key], in_place=True)

        # Merge with the output TimeSeries
        out_ts.merge(temp_ts, resample=True, in_place=True)

    # Scale time globally
    out_ts.time = (out_ts.time - time_range_in_pixels[0]) * (
        time_range[1] - time_range[0]
    ) / (time_range_in_pixels[1] - time_range_in_pixels[0]) + time_range[0]

    return out_ts
