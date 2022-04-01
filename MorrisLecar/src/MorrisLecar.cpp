#include "MorrisLecar.h"

#include "ap_axi_sdata.h"
#include "ap_int.h"
#include "hls_math.h"
#include "hls_stream.h"

void MorrisLecar(float Iext, data_t *V, data_t *W, float g_fast, float g_slow,
                 float beta_w) {
#pragma HLS INTERFACE s_axilite port = return
    data_t IL = G_LEAK * (*V - EL_M);
    data_t minf = 0.5 * (1 + hls::tanh((*V - BETA_M) / GAMMA_M));
    data_t winf = 0.5 * (1 + hls::tanh((*V - beta_w) / GAMMA_W));
    data_t tauw = 1 / hls::cosh(0.5 * (*V - beta_w) / GAMMA_W);
    data_t INa = g_fast * minf * (*V - ENa_M);
    data_t IK = g_slow * *W * (*V - EK_M);
    data_t dvdt = (Iext - IL - INa - IK) / CM_M;
    data_t dwdt = (winf - *W) * PHI / tauw;

    *V += dvdt * DT;
    *W += dwdt * DT;
}
#ifdef LUT
data_t tanh_apr(data_t x) {
    data_t ret = 1;
    if (hls::abs(x) < 3)
        ret = (x > 0) ? tanh_LUT[(int)x * 256] : -tanh_LUT[(int)x * 256];
    if (x < 0)
        ret = ret * -1;
    return ret;
}

data_t sech_apr(data_t x) {
    data_t ret = 0;
    if (hls::abs(x) < 6)
        ret = (x > 0) ? sech_LUT[(int)x * 256] : -sech_LUT[(int)x * 256];
    if (x < 0)
        ret = ret * -1;
    return ret;
}
#endif // LUT
