# flowpy
Python bindings for Flowy

## Installation from Source

```bash
micromamba create -f environment.yml # For the first time only
micromamba activate flowpyenv
meson setup build # To download flowy and C++ dependencies using meson wrap files
pip install .
```
If you have issues with `xtensor-python`, install it in the environment using:
```bash
micromamba install xtensor-python
```