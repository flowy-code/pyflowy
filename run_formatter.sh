#!/bin/sh 
find ./python_bindings -regex '.*\.\(cpp\|hpp\|cc\|cxx\)' -exec clang-format -i {} \;
find ./pyflowy -regex '.*py' -exec black {} \;
