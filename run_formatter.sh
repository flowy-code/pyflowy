#!/bin/sh 
find ./python_bindings -regex '.*\.\(cpp\|hpp\|cc\|cxx\)' -exec clang-format -i {} \;
find ./flowpy -regex '.*py' -exec black {} \;