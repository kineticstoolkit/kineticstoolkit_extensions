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
import kineticstoolkit as ktk
from kineticstoolkit_extensions import opensim

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


def test_run_scaling():
    """Test the scaling operation."""
    # !TODO Load something
    opensim.run_scaling()
    # !TODO Test something


def test_write_trc():
    """TODO."""
    pass


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
