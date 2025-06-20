# kineticstoolkit_extensions
Additional modules and development of new features for Kinetics Toolkit

This repository will replace the different repositories used for the current extension system. It will also be distributed via pip and conda, like kineticstoolkit.

It will contain features that are deemed too specific for Kinetics Toolkit, but still useful in some use cases. It will also contain half-baked new features in development. The main objective for this method is to:

- reach a stable 1.0 version for Kinetics Toolkit while continuing developing new features with a clear separation between misc/development/testing (kineticstoolkit_extensions) and stable (kineticstoolkit)
- ease the installation of extensions, without adding unnecessary friction both for developers and users (i.e. maintaining multiple repositories)
- adopt continuous integration practices (i.e. unit tests) for extensions, like for kineticstoolkit
