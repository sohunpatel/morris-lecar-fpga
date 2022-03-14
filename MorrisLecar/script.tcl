############################################################
## This file is generated automatically by Vitis HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2020 Xilinx, Inc. All Rights Reserved.
############################################################
open_project MorrisLecar
set_top MorrisLecar
add_files MorrisLecar/src/MorrisLecar.cpp
add_files MorrisLecar/src/MorrisLecar.h
open_solution "MorrisLecar" -flow_target vivado
set_part {xc7z020-clg400-1}
create_clock -period 10 -name default
config_export -format ip_catalog -output /home/sohun/IP/MorrisLecar.zip -rtl verilog
source "./MorrisLecar/MorrisLecar/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -flow impl -rtl verilog -format ip_catalog -output /home/sohun/IP/MorrisLecar.zip
