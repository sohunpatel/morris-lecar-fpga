import numpy as np
import math
import matplotlib.pyplot as plt
import LUTs


def main():
    N = 8
    tanhLUT = np.zeros((2**N + 1,), dtype=np.float32)
    sechLUT = np.zeros((2**N + 1,), dtype=np.float32)
    tanhBound = 5
    sechBound = 10
    for i in range(len(tanhLUT)):
        tanhLUT[i] = math.tanh(tanhBound*i/2**N)
    for i in range(len(sechLUT)):
        sechLUT[i] = 1 / math.cosh(sechBound*i/2**N)

    C = 2
    ELeak = -70
    ENa = 50
    EK = -100
    gLeak = 2
    gFast = 20
    gSlow = 20
    betaM = -1.2
    betaW = -13
    gammaM = 18
    gammaW = 10
    phi = 0.15
    dt = 0.1

    Iinj = 40 + 25*np.random.randn(1500)
    V = np.zeros(len(Iinj))
    Va = np.zeros(len(Iinj))
    W = np.zeros(len(Iinj))
    Wa = np.zeros(len(Iinj))

    V[0] = -70
    Va[0] = -70
    W[0] = 0.000025
    Wa[0] = 0.000025

    IL = np.zeros(len(Iinj))
    IFast = np.zeros(len(Iinj))
    ISlow = np.zeros(len(Iinj))
    ILa = np.zeros(len(Iinj))
    IFasta = np.zeros(len(Iinj))
    ISlowa = np.zeros(len(Iinj))

    i = 1
    while i < len(Iinj):
        mInf = 0.5 * (1 + math.tanh((V[i-1] - betaM) / gammaM))
        mInfa = 0.5 * \
            (1 + LUTs.tanh((Va[i-1] - betaM) / gammaM, tanhLUT, tanhBound))
        wInf = 0.5 * (1 + math.tanh((V[i-1] - betaW) / gammaW))
        wInfa = 0.5 * \
            (1 + LUTs.tanh((Va[i-1] - betaW) / gammaW, tanhLUT, tanhBound))
        tauW = 1 / math.cosh(0.5 * (V[i-1] - betaW) / gammaW)
        tauWa = LUTs.sech(
            0.5 * ((Va[i-1] - betaW) / gammaW), sechLUT, sechBound)
        IL[i] = gLeak * (V[i-1] - ELeak)
        ILa[i] = gLeak * (Va[i-1] - ELeak)
        IFast[i] = gFast * mInf * (V[i-1] - ENa)
        IFasta[i] = gFast * mInfa * (Va[i-1] - ENa)
        ISlow[i] = gSlow * W[i-1] * (V[i-1] - EK)
        ISlowa[i] = gSlow * Wa[i-1] * (Va[i-1] - EK)

        dwdt = phi * (wInf - W[i-1]) / tauW
        dwdta = phi * (wInfa - Wa[i-1]) / tauWa
        dvdt = (Iinj[i] - IL[i] - IFast[i] - ISlow[i]) / C
        dvdta = (Iinj[i] - ILa[i] - IFasta[i] - ISlowa[i]) / C

        W[i] = W[i-1] + dwdt * dt
        Wa[i] = Wa[i-1] + dwdta * dt
        V[i] = V[i-1] + dvdt * dt
        Va[i] = Va[i-1] + dvdta * dt

        i = i + 1

    V_plot, = plt.plot(V, label="tanh function")
    Va_plot, = plt.plot(Va, label="LUT")
    plt.xlabel("Time [ms]")
    plt.ylabel("Membrane Potential [mV]")
    plt.title("Comparison of using tanh function vs LUT")
    plt.legend(handles=[V_plot, Va_plot])
    plt.show()


if __name__ == "__main__":
    main()
