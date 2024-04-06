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

Please note, that you will need to delete directories downloaded by `meson` if you want to pull the latest commits of the dependencies. Please do not delete the wrap file for `flowy`. Here's what you should do:
```bash
micromamba activate flowpyenv
rm -rf subprojects/pdf_cpplib.wrap subprojects/flowy
meson setup build --wipe
pip install .
```