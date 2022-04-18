import pynq
import numpy as np
import Currents as I
import time

def sol(Iinj):
    A = 4*5^2
    C = 2
    ELeak = -70
    EK = -100
    ENa = 50
    gFast = 20
    gLeak = 2
    gSlow = 20
    betaM = -1.2
    betaW = -13
    gammaM = 18
    gammaW = 10
    phi = 0.15
    dt = 0.1
    V = np.zeros(len(Iinj))
    W = np.zeros(len(Iinj))

    V[0] = -70
    W[0] = 0.000025

    IL = np.zeros(len(Iinj))
    IFast = np.zeros(len(Iinj))
    ISlow = np.zeros(len(Iinj))
    
    start = time.time()

    i = 2
    while i < len(Iinj):
        IL[i] = I.leakage(V[i-1], gLeak, ELeak)
        IFast[i] = I.fast(V[i-1], gFast, ENa, betaM, gammaM)
        ISlow[i], wInf, tau_w = I.slow(V[i-1], W[i-1], gSlow, EK, betaW, gammaW)

        dwdt = phi*(wInf - W[i-1]) / tau_w
        dvdt = (Iinj[i] - IL[i] - IFast[i] - ISlow[i]) / C

        W[i] = W[i-1] + dwdt*dt
        V[i] = V[i-1] + dvdt*dt

        i = i + 1
        
    end = time.time()
    diff = end - start

    return V, diff