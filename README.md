# kineticstoolkit_extensions
Additional modules and development of new features for Kinetics Toolkit

This repository will replace the different repositories used for the current extension system. It will also be distributed via pip and conda, like kineticstoolkit.

It will contain features that are deemed too specific for Kinetics Toolkit, but still useful in some use cases. It will also contain new features in developement, before the features are integrated in the kineticstoolkit core. The main objective for this method is to:

- reach a stable 1.0 version for Kinetics Toolkit
- continue developing new features with a clear separation between development/testing (here) and stable (core)
- ease the installation of extensions, without adding unnecessary friction (i.e. maintaining multiple repositories)
- adopt continuous integration practices for extensions as for kineticstoolkit (i.e. unit tests)
