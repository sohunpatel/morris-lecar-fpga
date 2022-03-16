timedatectl set-ntp 0
timedatectl set-time 2020-04-16
/tools/Xilinx/Vitis/2020.1/bin/vitis_hls ./MorrisLecar/script.tcl
rm -rf ~/IP/MorrisLecar
unzip ~/IP/MorrisLecar.zip -d ~/IP/MorrisLecar
rm -rf ~/IP/MorrisLecar.zip
timedatectl set-ntp 1