# kineticstoolkit_extensions

Additional modules and development of new features for [Kinetics Toolkit](https://kineticstoolkit.uqam.ca)

This package provides modules that are not included straight into kineticstoolkit because either:

1. Their use case is specific to one research area of human movement biomechanics (e.g., pushrimkinetics).
2. They refer to specific or older hardware (e.g., n3d).
3. They are in active development and their API is not stable enough to be distributed in their final form.
4. They are not neutral - for example, they may relate to evolving assumptions on the human body, such as anthropometric tables or local coordinate system definitions based on bony landmarks.


## Current list of extensions

### Stable extensions

|  Extension                                                                                                                              |  Description                                                                                            |
|-----------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
|  [n3d](https://github.com/kineticstoolkit/kineticstoolkit_extensions/tree/main/kineticstoolkit_extensions/n3d)                          |  Provide `read_n3d()` to read Optotrak 3d acquisitions.                                                 |
|  [pushrimkinetics](https://github.com/kineticstoolkit/kineticstoolkit_extensions/tree/main/kineticstoolkit_extensions/pushrimkinetics)  |  Provide functions to process kinetic data from instrumented wheelchair wheels such as the SmartWheel.  |

### Currently in development

|  Extension                                                                                                                          |  Description                                                                                    |
|-------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
|  [video](https://github.com/kineticstoolkit/kineticstoolkit_extensions/tree/main/kineticstoolkit_extensions/video)                  |  Will allow reading video files to synchronize and add events to TimeSeries.                    |
|  [anthropometry](https://github.com/kineticstoolkit/kineticstoolkit_extensions/tree/main/kineticstoolkit_extensions/anthropometry)  |  Will allow estimating joint centres, centres of mass and generating local coordinate systems.  |

## Installing extensions

All extensions are included in the single `kineticstoolkit_extensions` package, which is installed like you installed `kineticstoolkit`, e.g., using pip or conda:

```
pip install kineticstoolkit_extensions
```

or

```
conda install -c conda-forge kineticstoolkit_extensions
```

⚠️ Warning: Individual extensions may require additional packages that are not installed by default. Consult the extension's documentation to know if such packages must be installed.


## Using extensions

Whereas all extensions are distributed in the same `kineticstoolkit_extensions` package, each extension is imported separately, following your needs. For instance, to calculate the velocity of a wheelchair wheel using the `pushrimkinetics` extension:

```
import kineticstoolkit_extensions.pushrimkinetics as pk

pk.calculate_velocity(ts)
```


## Developing extensions

If you wrote code that extends Kinetics Toolkit and you want to share it globally, consider sharing it as a Kinetics Toolkit extension. This is the best way to ensure that your code keeps functioning in the future, since extensions are tested automatically and continuously with each Kinetics Toolkit release.

**Step 1. Fork `kineticstoolkit_extensions`**

On GitHub, fork the [kineticstoolkit_extensions](https://github.com/kineticstoolkit/kineticstoolkit_extensions) repository.

**Step 2. Create a folder for your extension**

On your fork, add a new folder YOUR_EXTENSION_NAME in the `kineticstoolkit_extensions` folder.

**Step 3. Add your code and documentation**

On your fork, add:

- your code in `kineticstoolkit_extensions/YOUR_EXTENSION_NAME/__init__.py`. Take [n3d/__init__.py](https://github.com/kineticstoolkit/kineticstoolkit_extensions/blob/main/kineticstoolkit_extensions/n3d/__init__.py) as an example.
- your main documentation file in `kineticstoolkit_extensions/YOUR_EXTENSION_NAME/README.md`.
- if needed, one or several tutorials that showcase your extension.

**Step 4. Add your extension in this README**

On your fork, edit this `README.md` and add your extension in the "Stable extensions" table above.

**Step 5. Add unit tests**

A unit test is a function that is regularly run automatically. Writing unit tests is a great way to ensure that your extension will keep running in the long term on future versions of kineticstoolkit, on all three main platforms (Windows, MacOS, Linux) and on new versions of Python, because we get a notification the minute it fails.

A unit test generally checks that running a function with a given input generates what we expect, using the `assert` command.

On your fork, add a nest file named `kineticstoolkit_extensions/YOUR_EXTENSION_NAME/test_YOUR_EXTENSION_NAME.py`. Take [test_n3d.py](https://github.com/kineticstoolkit/kineticstoolkit_extensions/blob/main/kineticstoolkit_extensions/n3d/test_n3d.py) as an example. Each test function must begin with "test_".

Your can include (small) data files in a subfolder such as `kineticstoolkit_extensions/YOUR_EXTENSION_NAME/data`.

**Step 6. Run the unit tests**

First, run your unit test locally. You will need to install `pytest` for it.

When all the unit tests run successfully on your machine, commit your files and push to GitHub, then wait for the unit tests to be executed. If your unit tests do not pass, inspect the output on GitHub using "Details" and search for the error message. Use this error message to correct your unit test (and maybe also your tutorial), then commit and push again.


**Step 7. Create a Pull Request**

If all tests run successfully in your fork, create a Pull Request explaining what you added, and confirming that you have added a README and a well-functioning unit test. You will eventually get notified if changes are needed or if your pull request (PR) has been merged to the main `kineticstoolkit_extensions` repository.

In any step, do not hesitate to [ask for help](https://github.com/felixchenier/kineticstoolkit/discussions), it will be a pleasure to guide you.
