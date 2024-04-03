#define PYBIND11_DETAILED_ERROR_MESSAGES

#include "simulation.hpp"

// Bindings
#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// Namespaces
using namespace std::string_literals; // For ""s
using namespace pybind11::literals;   // For ""_a
namespace py = pybind11;              // Convention

int add(int a, int b) { return a + b; }

PYBIND11_MODULE(flowpycpp, m) {
  m.doc() = "Python bindings for flowy"; // optional module docstring

  m.def("add", &add, "A function that adds two numbers");
}