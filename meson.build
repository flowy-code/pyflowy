project('flowpy', 'cpp', 
  default_options : ['warning_level=3', 'cpp_std=c++20'])

args = []
deps = []

cppc = meson.get_compiler('cpp')

# If we want to build with netcdf we have to define this preprocessor variable
# otherwise the netcdf header will be empty
opt_with_netcdf = get_option('with_netcdf')
if opt_with_netcdf
  args += ['-DWITH_NETCDF']
endif

flowy_proj = subproject('flowy', default_options : ['with_netcdf=' + opt_with_netcdf.to_string()])
flowylib = flowy_proj.get_variable('flowylib_shared_dep')
deps += [flowylib]

py = import('python').find_installation('python', modules: ['numpy'])
deps += py.dependency()

# NumPy dependency
incdir_numpy = run_command(py,
  ['-c', 'import os; os.chdir(".."); import numpy; print(numpy.get_include())'],
  check : true
).stdout().strip()
inc_np = include_directories(incdir_numpy)
deps += declare_dependency(include_directories: inc_np)

pyb11_dep = [
  py.dependency(),
  dependency('pybind11')
]
deps += [pyb11_dep]

# for the bindings
py.extension_module(
  'flowpycpp',
  sources : [
    'python_bindings/bindings.cpp'
  ],
  include_directories: inc_np,
  dependencies: deps,
  cpp_args : args,
  install: true,
  subdir: 'flowpy/'
)


# flowpy main package
py.install_sources([
    'flowpy/__init__.py',
  ],
  pure: false, # install next to compiled extension
  subdir: 'flowpy'
)

# Util 
py.install_sources([
    'flowpy/util.py',
  ],
  pure: false,
  subdir: 'flowpy'
)
