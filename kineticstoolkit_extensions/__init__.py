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
Kinetics Toolkit Extensions.

Each extension is imported separately, for example::

    import kineticstoolkit_extensions.pushrimkinetics as pk

Installing kineticstoolkit_extensions does not install the possible additional
packages required by each extension. Please read the documentation of each
extension to know which additionnal package to install.

"""
__author__ = "Félix Chénier"
__copyright__ = "Copyright (C) 2020-2025 Félix Chénier"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"

import os

root_folder = os.path.dirname(os.path.dirname(__file__))
