open_project morris-lecar -reset
set_top MorrisLecar
add_files ./src/MorrisLecar.cpp
open_solution "solution1" -flow_target vivado
set_part {xc7z020-clg400-1}
create_clock -period 10 -name default
config_export -format ip_catalog -rtl verilog
set_directive_top -name morris-lecar "Morris Lecar"
csynth_design
export_design -flow syn -rtl verilog -format ip_catalog -description "Latency Monitor" -version "1.0" -display_name "Morris Lecar Neuron"
