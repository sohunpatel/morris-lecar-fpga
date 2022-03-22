#include "MorrisLecar.h"

#include "ap_axi_sdata.h"
#include "ap_int.h"
#include "hls_math.h"
#include "hls_stream.h"

void MorrisLecar(hls::stream<stream_param_t> &Iext,
                 hls::stream<stream_t> &V_out, data_t *V, data_t *W) {
#pragma HLS INTERFACE axis port = Iext
#pragma HLS INTERFACE axis port = V_out
#pragma HLS INTERFACE s_axilite port = return
#ifdef LUT
#pragma HLS ARRAY_PARTITION variable = tanh_LUT dim = 1
#pragma HLS ARRAY_PARTITION variable = sech_LUT dim = 1
#endif

    stream_t voltage;
    stream_param_t parameters;
    params_t params;
    converter_t mem_potent;
    while (!Iext.empty()) {
        Iext.read(parameters);
        params.total = parameters.data;

        data_t IL = G_LEAK * (*V - EL_M);
        data_t minf = 0.5 * (1 + hls::tanh((*V - BETA_M) / GAMMA_M));
        data_t winf = 0.5 * (1 + hls::tanh((*V - params.beta_w.f) / GAMMA_W));
        data_t tauw = 1 / hls::cosh(0.5 * (*V - params.beta_w.f) / GAMMA_W);
        data_t INa = params.g_fast.f * minf * (*V - ENa_M);
        data_t IK = params.g_slow.f * *W * (*V - EK_M);
        data_t dvdt = (params.i_inj.f - IL - INa - IK) / CM_M;
        data_t dwdt = (winf - *W) * PHI / tauw;

        *V += dvdt * DT;
        *W += dwdt * DT;
        mem_potent.f = *V;
        voltage.data = mem_potent.i;
        V_out.write(voltage);
    }
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
