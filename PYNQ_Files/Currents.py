import pynq
import numpy as np
import math

def leakage(V, g_leak, EL_M):
    return g_leak*(V - EL_M)

def fast(V, g_fast, ENa_m, Beta_m, Gamma_m):
    mInf = 0.5*(1+math.tanh((V - Beta_m)/Gamma_m))
    return g_fast*mInf*(V - ENa_m)

def slow(V, W, g_slow, EK, Beta_w, Gamma_w):
    wInf = 0.5*(1+math.tanh((V - Beta_w)/Gamma_w))
    tau_w = 1/math.cosh(0.5*(V - Beta_w)/Gamma_w)
    i = g_slow*W*(V - EK)
    return i, wInf, tau_w