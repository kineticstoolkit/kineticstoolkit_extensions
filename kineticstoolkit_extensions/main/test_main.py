#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2026 Félix Chénier

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
__copyright__ = "Copyright (C) 2026 Félix Chénier"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"


import kineticstoolkit_extensions as ext
import os


def test_all_modules_listed():
    """Test that all modules are either in available_modules or dev_modules."""
    all_module_folders = []
    for dirpath, dirnames, filenames in os.walk(
        f"{ext.root_folder}/kineticstoolkit_extensions"
    ):
        if "__init__.py" in filenames:
            all_module_folders.append(os.path.basename(dirpath))

    for module in all_module_folders:
        if module != "kineticstoolkit_extensions":
            if (module not in ext.available_modules) and (
                module not in ext.dev_modules
            ):
                raise ValueError(f"Module {module} not listed.")


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
