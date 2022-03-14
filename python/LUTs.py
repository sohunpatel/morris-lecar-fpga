import numpy as np
from math import trunc
import math


def tanh(x: float, LUT, bound):
    N = math.log2(len(LUT)-1)
    retval = 1
    if abs(x) < bound:
        retval = LUT[trunc(abs(x) * 2**N / bound)]
    if x < 0:
        retval = retval * -1
    return retval


def sech(x: float, LUT, bound):
    N = math.log2(len(LUT)-1)
    retval = 0.0005
    if abs(x) < bound:
        retval = LUT[trunc(abs(x) * 2**N / bound)]
    return retval


if __name__ == "__main__":
    required_precision = 0.0001
    N = 1
    current_error = 1

    tanhBound = 0
    sechBound = 0
    while math.tanh(tanhBound) < 1 - required_precision:
        tanhBound = tanhBound + 1
    while (1/math.cosh(sechBound)) > required_precision:
        sechBound = sechBound + 1

    while current_error > required_precision:
        tanh_error = 0
        sech_error = 0
        tanhLUT = np.zeros((2**N)+1)
        sechLUT = np.zeros((2**N)+1)
        for n in range(len(tanhLUT)):
            tanhLUT[n] = math.tanh(tanhBound*n/2**N)
        for n in range(len(sechLUT)):
            sechLUT[n] = 1 / math.cosh(sechBound*n/2**N)
        evaluation = 0
        for n in range(len(tanhLUT)):
            x = tanhBound*n/(2**N) - required_precision
            evaluation = abs(math.tanh(x) - tanh(x, tanhLUT, tanhBound))
            if evaluation > tanh_error:
                tanh_error = evaluation
        evaluation = 0
        for n in range(len(sechLUT)):
            x = sechBound*n/(2**N) - required_precision
            evaluation = abs(1/math.cosh(x) - sech(x, sechLUT, sechBound))
            if evaluation > sech_error:
                sech_error = evaluation
        current_error = max(sech_error, tanh_error)
        if (N >= 32):
            break
        N = N + 1
    print("Lenth of LUT: ", N-1)
