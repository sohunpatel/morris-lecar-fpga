create_project pynq-interface ./pynq-interface -part xc7z020-clg400-1 -force
# set_property board_part xilinx.com:au250:part0:1.3 [current_project]
set_property ip_repo_paths ../ip/ [current_project]
update_ip_catalog
source top.tcl
make_wrapper -files [get_files ./pynq-interface/pynq-interface.srcs/sources_1/bd/top/top.bd] -top
#add_files -norecurse ./latency_monitor/latency_monitor.srcs/sources_1/bd/top/hdl/top_wrapper.v
add_files -norecurse ./pynq-interface/pynq-interface.srcs/sources_1/bd/top/hdl/top_wrapper.v
launch_runs impl_1 -to_step write_bitstream -jobs 10
wait_on_run impl_1
if {[file exists ../PYNQ_Files/top.bit] == 1} {
    file delete ../PYNQ_Files/top.bit
}
file copy ./pynq-interface/pynq-interface.runs/impl_1/top_wrapper.bit ../PYNQ_Files/top.bit
