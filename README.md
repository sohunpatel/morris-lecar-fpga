# Morris Lecar on FPGA

Implementation of 2-dimensional Morris Lecar neuron model equations on digital hardware. This project creates IP that evaluates the membrane potential of the neuron. The IP can be used to create an network, but needs an interface to be interactable.

### Requirements

* Vitis HLS 2020.1
* Vivado 2020.1
* TCL > 8.0.0
* GCC > 9.0.0

Note that all development was done on Ubuntu 20.04.

### Usage

To run synthesis and export the IP, run the run.sh file. Note that you may have to edit the vitis_hls file locations depending on your system and the location of the binary on your system.
