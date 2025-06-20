import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("kineticstoolkit_extensions/VERSION", "r") as fh:
    version = fh.read()


setuptools.setup(
    name="kineticstoolkit_extensions",
    version=version,
    description="Extensions and unstable development modules for Kinetics Toolkit.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://kineticstoolkit.uqam.ca",
    author="Félix Chénier",
    author_email="chenier.felix@uqam.ca",
    license="Apache",
    license_files=["LICENSE.txt", "NOTICE.txt"],
    packages=setuptools.find_packages(),
    package_data={
        "kineticstoolkit_extensions": ["VERSION"],
    },
    project_urls={
        "Documentation": "https://kineticstoolkit.uqam.ca",
        "Source": "https://github.com/kineticstoolkit/kineticstoolkit_extensions",
        "Tracker": "https://github.com/kineticstoolkit/kineticstoolkit/issues",
    },
    install_requires=["kineticstoolkit"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.10",
)
