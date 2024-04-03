project('flowpy', 'cpp', 
  default_options : ['warning_level=3', 'cpp_std=c++20'])

args = []
deps = []

flowy_proj = subproject('flowy')
flowylib = flowy_proj.get_variable('flowylib_dep')
deps += [flowylib]

py_mod = import('python')
py = py_mod.find_installation(pure: false)

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