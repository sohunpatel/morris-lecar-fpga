# Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Project Directory](#project-directory)
- [Usage](#usage)
  - [Requirements](#requirements)
  - [Setup PYNQ](#setup-pynq)
- [Troubleshooting](#troubleshooting)
  - [Vitis unrecognized files](#vitis-unrecognized-files)
  - [Vitis fails when trying to export ip](#vitis-fails-when-trying-to-export-ip)
  - [Unable to view the PYNQ jupyter server](#unable-to-view-the-pynq-jupyter-server)

# Introduction

This project explores the implementation of the reduced 2-dimensional Morris Lecar neuronal dynamics equations on digital hardware. There have been recent developments in neuromorphic hardware, most of which use the Leaky Integrate and Fire (LIF) model. This is a great option for neuromorphic hardware because of its simplicity tp implement in digital hardware. What is does lack is accuracy to our most robust biological models. 

# Project Directory
```
. 
├── ip/                     # Vitis HLS IP for use in Vivado project
├───── morris-lecar/            # HLS IP for morris lecar neuron model
├──────── src/                      # Sources files that IP is generated from
├──────── run.sh                    # script that builds IP
├── pynq-interface/         # Vivado project to create the AXI interface to the IP
├───── pynq-interface.bit       # Bitstream created by vivado to be loaded onto pynq board
├───── run.tcl                  # TCL script to be run by vivado to build bitstream
├── PYNQ_Files/             # Files that should be copied to the PYNQ ARM environment
├───── comparison.ipynb         # Jupyter notebook that showcases the difference between hardware and software solutions
├───── Currents.py              # Script that contains functions to give software currents
├───── hardware.ipynb           # Jupyter notebook that showcases hardware solution
├───── hardware.py              # Script that contains function to return voltage for hardware solution
├───── software.ipynb           # Jupyter notebook that showcases software solution
├───── software.py              # Script that contains function to return voltage for software solution
├── python/                 # Random pythons tests and scripts
├── LICENSE
└── README.md
```

# Usage

To use this project, there are a few steps that need to be followed. It is recommended to use a linux OS, but a windows os can still be used with Ubuntu WSL.

1. Install software [requirements](#requirements) below on your host machine (laptop or desktop)
2. Source the settings for vitis by running `source XILINX_INSTALL_LOCATION/Vitis/2020.1/settings.sh`
3. Create HLS IP by running script [`ip/morris-lecar/run.sh`](ip/morris-lecar/run.sh)
4. Source the settings for vivado by running `source XILINX_INSTALL_LOCATION/Vivado/2020.1/settings.sh`
5. Generate bitstream by running script 'vivado pynq-interface/run.tcl'
4. [Setup PYNQ](#setup-pynq)

## Requirements

* OS: Ubuntu 20.04 (recommended) or Windows 10 with Ubuntu WSL
* Vitis (Vivado) HLS <= 2020.1
* Vivado <= 2020.1
* TCL > 8.0.0
* GCC > 9.0.0

## Setup PYNQ

To run the IP on a PYNQ board you will need a few things:

* PYNQ compatible FPGA development board
* [PYNQ v2.7 image](http://www.pynq.io/board.html) for your board
* micro SD card
* Ethernet cable
* Power supply or USB cable
* Image writer such as [balenaEtcher](https://www.balena.io/etcher/)

To get up and running with PYNQ:

1. Flash the PYNQ image to the sd card
2. Insert the SD card to the board, plug in power supply or USB, and power on
3. Connect board to router or host machine via ethernet
4. If ethernet is plugged directly into host machine, assign a static IP address of 192.168.2.1 (subnet mask of 255.255.255.0) to your ethernet adapter 
5. Open your browser and go to 192.168.2.99:9090 or pynq:9090
6. Open you file browser and open `\\192.168.2.99\xilinx\` in the top browser
7. Copy the files in `PYNQ_FILES` to the `jupyter_notebooks` directory on the PYNQ ARM environment
8. Now, you can run the notebooks

The default username and password for the PYNQ jupyter server is xilinx.

# Troubleshooting

## Vitis unrecognized files

Because tcl uses absolute file paths, you may need to edit the files defined in [`scripts.tcl`](MorrisLecar/MorrisLecar/script.tcl) to match the absolute file paths on your system

## Vitis fails when trying to export ip

This is most likely due to the system time. For some reason, Vitis requires the time to be in 2020 for licencing reasons. The scripts to generate the ip should take care of this, but if that is not working, change the time on your system manually.

## Unable to view the PYNQ jupyter server

There are a few things that might be wrong. If possible connect to USB to your host machine and open a terminal on that port using PuTTY or minicom. Then, you should be able to view the boot-up sequence. If there is a failure in the boot-up sequence, it is most likely from an error when writing the image. Make sure that you are using PYNQ v2.7 from the [link]((http://www.pynq.io/board.html)) above.

There is a specific sequence of events that will tell you if the sequence has occurred properly if you cannot connect to the usb port. It may change depending on your board, but generally a green LED labeled "Done" will turn on and some other LEDs will flash a few times.

If the correct boot-up sequence occurred, but you still cannot access the jupyter server, the problem most likely is with the connection on the host machine. Sometimes, different browsers will not work with PYNQ. It is recommened that a chromium based browser is used such as Google Chrome or Microsoft Edge. Also, make sure that your ethernet adapter has been assigned a static IP address. For windows, follow this [guidelines](https://kb.netgear.com/27476/How-do-I-set-a-static-IP-address-in-Windows), for linux this [guidelines](https://sites.cns.utexas.edu/oit-blog/blog/how-set-static-ip-linux-machine).
