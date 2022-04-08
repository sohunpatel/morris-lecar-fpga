import os
from sys import platform

if platform == "linux" or platform == "linux2":
    os.system("timedatectl set-ntp 0")
    os.system("timedatectl set-time 2020-01-01")
    os.system("/tools/Xilinx/Vitis/2020.1/bin/vitis_hls ./MorrisLecar/script.tcl")
    os.system("rm -rf ../IP/MorrisLecar")
    os.system("unzip ../IP/MorrisLecar.zip -d ../IP/MorrisLecar")
    os.system("rm -rf ../IP/MorrisLecar.zip")
elif platform == "win32":
    os.system("")