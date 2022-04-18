from pynq import Overlay
from pynq import allocate
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import *
import time

def sol(Iinj):
    ol = Overlay("./top.bit")

    dma = ol.axi_dma_0
    dma_send = ol.axi_dma_0.sendchannel
    dma_recv = ol.axi_dma_0.recvchannel
    hls_ip = ol.MorrisLecar_0

    CONTROL_REGISTER = 0x0
    hls_ip.write(CONTROL_REGISTER, 0x81) # 0x81 will set bit 0

    data_size = len(Iinj)
    input_buffer = allocate(shape=(data_size,), dtype=np.float32)
    
    for i in range(data_size):
        input_buffer[i] = np.float32(Iinj[i]);
        
    start = time.time()
    
    dma_send.transfer(input_buffer)
    
    output_buffer = allocate(shape=(data_size,), dtype=np.float32)
    dma_recv.transfer(output_buffer)
    
    end = time.time()
    diff = end - start
    
    return output_buffer, diff