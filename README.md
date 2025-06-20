# kineticstoolkit_extensions
Additional modules and development of new features for Kinetics Toolkit

This package provides modules that are not included straight into kineticstoolkit because either:

1. Their use case is specific to one research area of human movement biomechanics (e.g., pushrimkinetics)
2. They refer to unused or older hardware (e.g., n3d)
3. They are in active development and their API is not stable enough to be distributed in their final form
4. They are not neutral - for example, they may relate to assumptions on the human body, such as anthropometric tables or local coordinate systems based on bony landmarks.

To install:

```
pip install kineticstoolkit_extensions
```

or

```
conda install -c conda-forge kineticstoolkit_extensions
```

The published extensions all have unit tests so that they are continually tested and expected to work in future versions of Python.


## Stable extensions

[pushrimkinetics](tutorials/pushrimkinetics.ipynb) - Allow reading and processing kinetics recorded by instrumented wheelchair wheels such as SmartWheel.

n3d - Allow reading n3d file from NDI Optotrak.


## Currently in development

video - Will allow reading video files, synchronize those videos with other TimeSeries, and use the videos to add events to these TimeSeries. You need to install opencv to use this module.
