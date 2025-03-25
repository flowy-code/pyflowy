#include "flowy/include/asc_file.hpp"
#include "flowy/include/config.hpp"
#include "flowy/include/config_parser.hpp"
#include "flowy/include/definitions.hpp"
#include "flowy/include/lobe.hpp"
#include "flowy/include/models/mr_lava_loba.hpp"
#include "flowy/include/simulation.hpp"
#include "flowy/include/topography.hpp"
#include "flowy/include/topography_file.hpp"
#include "pybind11/detail/common.h"
#include "pybind11/pytypes.h"

#ifdef WITH_NETCDF
#include "flowy/include/netcdf_file.hpp"
#endif

#define PYBIND11_DETAILED_ERROR_MESSAGES

// Bindings
#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl/filesystem.h>

// xtensor extensions
#define FORCE_IMPORT_ARRAY
#include "xtensor-python/pyarray.hpp"

// Namespaces
using namespace std::string_literals; // For ""s
using namespace pybind11::literals;   // For ""_a
namespace py = pybind11;              // Convention

PYBIND11_MODULE( flowycpp, m )
{
    xt::import_numpy();
    m.doc() = "Python bindings for flowy"; // optional module docstring

    py::class_<std::filesystem::path>( m, "Path" ).def( py::init<std::string>() );

    py::implicitly_convertible<std::string, std::filesystem::path>();

    py::class_<Flowy::TopographyCrop>( m, "TopographyCrop" )
        .def( py::init<>() )
        .def_readwrite( "x_min", &Flowy::TopographyCrop::x_min )
        .def_readwrite( "x_max", &Flowy::TopographyCrop::x_max )
        .def_readwrite( "y_min", &Flowy::TopographyCrop::y_min )
        .def_readwrite( "y_max", &Flowy::TopographyCrop::y_max );

    py::enum_<Flowy::OutputQuantity>( m, "OutputQuantity" )
        .value( "Hazard", Flowy::OutputQuantity::Hazard )
        .value( "Height", Flowy::OutputQuantity::Height );

    py::class_<Flowy::AscFile>( m, "AscFile" )
        .def( py::init<>() )
        .def( py::init<Flowy::Topography, Flowy::OutputQuantity>() )
        .def( py::init<std::filesystem::path>(), "file_path"_a )
        .def( py::init<std::filesystem::path, Flowy::TopographyCrop>() )
        .def( "save", &Flowy::AscFile::save )
        .def( "lower_left_corner", &Flowy::AscFile::lower_left_corner )
        .def( "cell_size", &Flowy::AscFile::cell_size )
        .def( "to_topography", &Flowy::AscFile::to_topography )
        .def( "crop_to_content", &Flowy::AscFile::crop_to_content )
        .def_readwrite( "no_data_value", &Flowy::AscFile::no_data_value )
        .def_readwrite( "data", &Flowy::AscFile::data )
        .def_readwrite( "x_data", &Flowy::AscFile::x_data )
        .def_readwrite( "y_data", &Flowy::AscFile::y_data )
        .def( "__repr__", []( const Flowy::AscFile & ) { return "<AscFile>"; } );

#ifdef WITH_NETCDF
    py::class_<Flowy::NetCDFFile>( m, "NetCDFFile" )
        .def( py::init<>() )
        .def( py::init<Flowy::Topography, Flowy::OutputQuantitiy>() )
        .def( py::init<std::filesystem::path>(), "file_path"_a )
        .def( py::init<std::filesystem::path, Flowy::TopographyCrop>() )
        .def( "save", &Flowy::NetCDFFile::save )
        .def( "lower_left_corner", &Flowy::NetCDFFile::lower_left_corner )
        .def( "cell_size", &Flowy::NetCDFFile::cell_size )
        .def( "to_topography", &Flowy::NetCDFFile::to_topography )
        .def( "crop_to_content", &Flowy::NetCDFFile::crop_to_content )
        .def_readwrite( "no_data_value", &Flowy::NetCDFFile::no_data_value )
        .def_readwrite( "data", &Flowy::NetCDFFile::data )
        .def_readwrite( "x_data", &Flowy::NetCDFFile::x_data )
        .def_readwrite( "y_data", &Flowy::NetCDFFile::y_data )
        .def( "__repr__", []( const Flowy::NetCDFFile & ) { return "<NetCDFFile>"; } );
#endif

    py::class_<Flowy::Lobe>( m, "Lobe" )
        .def( py::init<>() )
        .def_readwrite( "center", &Flowy::Lobe::center )
        .def_readwrite( "semi_axes", &Flowy::Lobe::semi_axes )
        .def_readwrite( "dist_n_lobes", &Flowy::Lobe::dist_n_lobes )
        .def_readwrite( "n_descendents", &Flowy::Lobe::n_descendents )
        .def_readwrite( "idx_parent", &Flowy::Lobe::idx_parent )
        .def_readwrite( "alpha_inertial", &Flowy::Lobe::alpha_inertial )
        .def_readwrite( "thickness", &Flowy::Lobe::thickness )
        .def( "area", &Flowy::Lobe::area )
        .def( "volume", &Flowy::Lobe::volume )
        .def( "set_azimuthal_angle", &Flowy::Lobe::set_azimuthal_angle )
        .def( "get_azimuthal_angle", &Flowy::Lobe::get_azimuthal_angle )
        .def( "get_sin_azimuthal_angle", &Flowy::Lobe::get_sin_azimuthal_angle )
        .def( "get_cos_azimuthal_angle", &Flowy::Lobe::get_cos_azimuthal_angle )
        .def( "extent_xy", &Flowy::Lobe::extent_xy )
        .def( "line_segment_intersects", &Flowy::Lobe::line_segment_intersects )
        .def( "is_point_in_lobe", &Flowy::Lobe::is_point_in_lobe )
        .def( "point_at_angle", py::overload_cast<double>( &Flowy::Lobe::point_at_angle, py::const_ ) )
        .def( "point_at_angle", py::overload_cast<double, double>( &Flowy::Lobe::point_at_angle, py::const_ ) )
        .def( "rasterize_perimeter", &Flowy::Lobe::rasterize_perimeter );

    py::class_<Flowy::LobeCells>( m, "LobeCells" )
        .def( py::init<>() )
        .def_readwrite( "cells_intersecting", &Flowy::LobeCells::cells_intersecting )
        .def_readwrite( "cells_enclosed", &Flowy::LobeCells::cells_enclosed );

    py::class_<Flowy::Topography>( m, "Topography" )
        .def( py::init<>() )
        .def( py::init<Flowy::MatrixX, Flowy::VectorX, Flowy::VectorX, double>() )
        .def_readwrite( "height_data", &Flowy::Topography::height_data )
        .def_readwrite( "x_data", &Flowy::Topography::x_data )
        .def_readwrite( "y_data", &Flowy::Topography::y_data )
        .def_readwrite( "no_data_value", &Flowy::Topography::no_data_value )
        .def( "cell_size", &Flowy::Topography::cell_size )
        .def( "height_and_slope", &Flowy::Topography::height_and_slope )
        .def( "get_cells_intersecting_lobe", &Flowy::Topography::get_cells_intersecting_lobe )
        .def( "compute_intersection", &Flowy::Topography::compute_intersection )
        .def( "add_lobe", &Flowy::Topography::add_lobe )
        .def( "is_point_near_boundary", &Flowy::Topography::is_point_near_boundary )
        .def( "locate_point", &Flowy::Topography::locate_point )
        .def( "find_preliminary_budding_point", &Flowy::Topography::find_preliminary_budding_point )
        .def( "bounding_box", &Flowy::Topography::bounding_box );

    py::class_<Flowy::Topography::BoundingBox>( m, "TopographyBoundingBox" )
        .def( py::init<>() )
        .def_readwrite( "idx_x_lower", &Flowy::Topography::BoundingBox::idx_x_lower )
        .def_readwrite( "idx_y_lower", &Flowy::Topography::BoundingBox::idx_y_lower )
        .def_readwrite( "idx_x_higher", &Flowy::Topography::BoundingBox::idx_x_higher )
        .def_readwrite( "idx_y_higher", &Flowy::Topography::BoundingBox::idx_y_higher );

    py::enum_<Flowy::StorageDataType>( m, "StorageDataType" )
        .value( "Short", Flowy::StorageDataType::Short )
        .value( "Float", Flowy::StorageDataType::Float )
        .value( "Double", Flowy::StorageDataType::Double );

    py::class_<Flowy::Config::OutputSettings>( m, "OutputSettings" )
        .def( py::init<>() )
        .def_readwrite( "crop_to_content", &Flowy::Config::OutputSettings::crop_to_content )
        .def_readwrite( "use_netcdf", &Flowy::Config::OutputSettings::use_netcdf )
        .def_readwrite( "compression", &Flowy::Config::OutputSettings::compression )
        .def_readwrite( "compression_level", &Flowy::Config::OutputSettings::compression_level )
        .def_readwrite( "shuffle", &Flowy::Config::OutputSettings::shuffle )
        .def_readwrite( "data_type", &Flowy::Config::OutputSettings::data_type );

    py::class_<Flowy::Config::InputParams>( m, "InputParams" )
        .def( py::init<>() )
        .def_readwrite( "output_folder", &Flowy::Config::InputParams::output_folder )
        .def_readwrite( "output_settings", &Flowy::Config::InputParams::output_settings )
        .def_readwrite("write_lobes_csv", &Flowy::Config::InputParams::write_lobes_csv)
        .def_readwrite("print_remaining_time", &Flowy::Config::InputParams::print_remaining_time)
        .def_readwrite("save_final_dem", &Flowy::Config::InputParams::save_final_dem)
        .def_readwrite("write_thickness_every_n_lobes", &Flowy::Config::InputParams::write_thickness_every_n_lobes)
        .def_readwrite("masking_tolerance", &Flowy::Config::InputParams::masking_tolerance)
        .def_readwrite("masking_max_iter", &Flowy::Config::InputParams::masking_max_iter)
        .def_readwrite("rng_seed", &Flowy::Config::InputParams::rng_seed)
        .def_readwrite("volume_correction", &Flowy::Config::InputParams::volume_correction)
        .def_readwrite( "run_name", &Flowy::Config::InputParams::run_name )
        .def_readwrite( "source", &Flowy::Config::InputParams::source )
        .def_readwrite( "vent_coordinates", &Flowy::Config::InputParams::vent_coordinates )
        .def("n_vents", &Flowy::Config::InputParams::n_vents)
        .def_readwrite( "save_hazard_data", &Flowy::Config::InputParams::save_hazard_data )
        .def_readwrite( "n_flows", &Flowy::Config::InputParams::n_flows )
        .def_readwrite( "n_lobes", &Flowy::Config::InputParams::n_lobes )
        .def_readwrite( "thickening_parameter", &Flowy::Config::InputParams::thickening_parameter )
        .def_readwrite( "prescribed_lobe_area", &Flowy::Config::InputParams::prescribed_lobe_area )
        .def_readwrite( "prescribed_avg_lobe_thickness", &Flowy::Config::InputParams::prescribed_avg_lobe_thickness )
        .def_readwrite("masking_threshold", &Flowy::Config::InputParams::masking_threshold)
        .def_readwrite( "min_n_lobes", &Flowy::Config::InputParams::min_n_lobes )
        .def_readwrite( "max_n_lobes", &Flowy::Config::InputParams::max_n_lobes )
        .def_readwrite( "inertial_exponent", &Flowy::Config::InputParams::inertial_exponent )
        .def_readwrite( "lobe_exponent", &Flowy::Config::InputParams::lobe_exponent )
        .def_readwrite( "max_slope_prob", &Flowy::Config::InputParams::max_slope_prob )
        .def_readwrite( "thickness_ratio", &Flowy::Config::InputParams::thickness_ratio )
        .def_readwrite( "fixed_dimension_flag", &Flowy::Config::InputParams::fixed_dimension_flag )
        .def_readwrite( "vent_flag", &Flowy::Config::InputParams::vent_flag )
        .def_readwrite( "fissure_end_coordinates", &Flowy::Config::InputParams::fissure_end_coordinates )
        .def_readwrite( "fissure_probabilities", &Flowy::Config::InputParams::fissure_probabilities )
        .def_readwrite( "total_volume", &Flowy::Config::InputParams::total_volume )
        .def_readwrite( "east_to_vent", &Flowy::Config::InputParams::east_to_vent )
        .def_readwrite( "west_to_vent", &Flowy::Config::InputParams::west_to_vent )
        .def_readwrite( "south_to_vent", &Flowy::Config::InputParams::south_to_vent )
        .def_readwrite( "north_to_vent", &Flowy::Config::InputParams::north_to_vent )
        .def_readwrite( "channel_file", &Flowy::Config::InputParams::channel_file )
        .def_readwrite( "alpha_channel", &Flowy::Config::InputParams::alfa_channel )
        .def_readwrite( "d1", &Flowy::Config::InputParams::d1 )
        .def_readwrite( "d2", &Flowy::Config::InputParams::d2 )
        .def_readwrite( "eps", &Flowy::Config::InputParams::eps )
        .def_readwrite( "union_diff_file", &Flowy::Config::InputParams::union_diff_file )
        .def_readwrite( "npoints", &Flowy::Config::InputParams::npoints )
        .def_readwrite( "n_init", &Flowy::Config::InputParams::n_init )
        .def_readwrite( "dist_fact", &Flowy::Config::InputParams::dist_fact )
        .def_readwrite( "flag_threshold", &Flowy::Config::InputParams::flag_threshold )
        .def_readwrite( "a_beta", &Flowy::Config::InputParams::a_beta )
        .def_readwrite( "b_beta", &Flowy::Config::InputParams::b_beta )
        .def_readwrite( "max_aspect_ratio", &Flowy::Config::InputParams::max_aspect_ratio )
        .def_readwrite( "aspect_ratio_coeff", &Flowy::Config::InputParams::aspect_ratio_coeff )            
        .def_readwrite( "restart_files", &Flowy::Config::InputParams::restart_files )
        .def_readwrite( "restart_filling_parameters", &Flowy::Config::InputParams::restart_filling_parameters );

    py::class_<Flowy::CommonLobeDimensions>( m, "CommonLobeDimensions" )
        .def( py::init<>() )
        .def( py::init<Flowy::Config::InputParams>() )
        .def_readwrite( "avg_lobe_thickness", &Flowy::CommonLobeDimensions::avg_lobe_thickness )
        .def_readwrite( "lobe_area", &Flowy::CommonLobeDimensions::lobe_area )
        .def_readwrite( "max_semiaxis", &Flowy::CommonLobeDimensions::max_semiaxis )
        .def_readwrite( "thickness_min", &Flowy::CommonLobeDimensions::thickness_min );

    py::class_<Flowy::Simulation>( m, "Simulation" )
        .def( py::init<Flowy::Config::InputParams, std::optional<int>>() )
        .def_readwrite( "input", &Flowy::Simulation::input )
        .def_readwrite( "topography", &Flowy::Simulation::topography )
        .def_readwrite( "lobes", &Flowy::Simulation::lobes )
        .def( "stop_condition", &Flowy::Simulation::stop_condition )
        .def( "run", &Flowy::Simulation::run );

    py::class_<Flowy::MrLavaLoba>( m, "MrLavaLoba" )
        .def_readwrite( "lobe_dimensions", &Flowy::MrLavaLoba::lobe_dimensions )
        .def( "compute_initial_lobe_position", &Flowy::MrLavaLoba::compute_initial_lobe_position )
        .def( "compute_lobe_axes", &Flowy::MrLavaLoba::compute_lobe_axes )
        .def( "compute_descendent_lobe_position", &Flowy::MrLavaLoba::compute_descendent_lobe_position )
        .def( "perturb_lobe_angle", &Flowy::MrLavaLoba::perturb_lobe_angle )
        .def( "select_parent_lobe", &Flowy::MrLavaLoba::select_parent_lobe )
        .def( "add_inertial_contribution", &Flowy::MrLavaLoba::add_inertial_contribution );

    m.def(
        "parse_config", &Flowy::Config::parse_config, "A function to parse input settings from a TOML file.",
        "config_path"_a );
}
