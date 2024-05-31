#!/bin/bash

# Directories of interest
PROJECT_DIR="${1:-$PWD}"
PYTHON_SITEPKGS=$(python -c 'import site; print(site.getsitepackages()[0])')

# Versions
XTL_VERSION='0.7.7'
XTENSOR_VERSION='0.25.0'
XTENSOR_BLAS_VERSION='0.21.0'
XTENSOR_PYTHON_VERSION='0.27.0'
NETCDF_VERSION='4.9.0'
FMT_VERSION='10.2.1'
COMMON_CMAKE='-DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release -DCMAKE_POSITION_INDEPENDENT_CODE=TRUE -DBUILD_SHARED_LIBS=OFF'

# Function to download, extract, and rename directory
download_and_rename() {
    local url=$1
    local dest_dir=$2
    local new_name=$3

    curl -L $url | tar -xzC /tmp
    mv /tmp/$dest_dir /tmp/$new_name
}

# Grab and install fmt
download_and_rename "https://github.com/fmtlib/fmt/archive/refs/tags/${FMT_VERSION}.tar.gz" "fmt-${FMT_VERSION}" "build-fmt"
cmake -S /tmp/build-fmt -B /tmp/build-fmt/build -DFMT_TEST=OFF ${COMMON_CMAKE}
cmake --build /tmp/build-fmt/build --target install
rm -rf /tmp/build-fmt

# TODO(rg): Probably worthwhile to grab xsimd
# Grab and install xtl
download_and_rename "https://github.com/xtensor-stack/xtl/archive/refs/tags/${XTL_VERSION}.tar.gz" "xtl-${XTL_VERSION}" "build-xtl"
cmake -S /tmp/build-xtl -B /tmp/build-xtl/build ${COMMON_CMAKE}
cmake --build /tmp/build-xtl/build --target install
rm -rf /tmp/build-xtl

# Grab and install xtensor
download_and_rename "https://github.com/xtensor-stack/xtensor/archive/refs/tags/${XTENSOR_VERSION}.tar.gz" "xtensor-${XTENSOR_VERSION}" "build-xtensor"
cmake -S /tmp/build-xtensor -B /tmp/build-xtensor/build ${COMMON_CMAKE}
cmake --build /tmp/build-xtensor/build --target install
rm -rf /tmp/build-xtensor

# Grab and install xtensor-blas from HaoZeke's fork
# Replace with upstream after https://github.com/xtensor-stack/xtensor-blas/pull/243
# Also remove -DVERSION then, when a tagged release is used
download_and_rename "https://github.com/HaoZeke/xtensor-blas/archive/refs/heads/addPkgConfig.tar.gz" "xtensor-blas-addPkgConfig" "build-xtblas"
cmake -S /tmp/build-xtblas -B /tmp/build-xtblas/build -DVERSION=${XTENSOR_BLAS_VERSION} ${COMMON_CMAKE}
cmake --build /tmp/build-xtblas/build --target install
rm -rf /tmp/build-xtblas

# xtensor-python needs these
pip install pybind11 numpy

# Set CMAKE_PREFIX_PATH
export CMAKE_PREFIX_PATH="${CMAKE_PREFIX_PATH}:${PYTHON_SITEPKGS}"

# Grab and install xtensor-python from HaoZeke's fork
# Replace with upstream after https://github.com/xtensor-stack/xtensor-python/pull/243
download_and_rename "https://github.com/HaoZeke/xtensor-python/archive/refs/heads/addPkgConfig.tar.gz" "xtensor-python-addPkgConfig" "build-xtpy"
cmake -S /tmp/build-xtpy -B /tmp/build-xtpy/build ${COMMON_CMAKE}
cmake --build /tmp/build-xtpy/build --target install
rm -rf /tmp/build-xtpy

unset CMAKE_PREFIX_PATH

# Build static NetCDF library
curl -L https://github.com/Unidata/netcdf-c/archive/refs/tags/v${NETCDF_VERSION}.tar.gz | tar -xzC /tmp
mkdir /tmp/build-netcdf
if [ "$(getconf LONG_BIT)" -ge 64 ]; then
    CDF5_OPTION='-DENABLE_CDF5=ON'
else
    CDF5_OPTION='-DENABLE_CDF5=OFF'
fi
cmake -S /tmp/netcdf-c-${NETCDF_VERSION} -B /tmp/build-netcdf ${COMMON_CMAKE} ${CDF5_OPTION} -DBUILD_TESTING=OFF -DBUILD_TESTSETS=OFF -DBUILD_UTILITIES=OFF -DENABLE_DAP=OFF -DENABLE_NETCDF4=OFF -DENABLE_NETCDF_4=OFF -DENABLE_PLUGINS=OFF
cmake --build /tmp/build-netcdf --target install
rm -rf /tmp/build-netcdf /tmp/netcdf-c-${NETCDF_VERSION}
