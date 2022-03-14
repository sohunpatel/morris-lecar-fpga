#include "MorrisLecar.h"

#include "ap_axi_sdata.h"
#include "ap_int.h"
#include "hls_math.h"
#include "hls_stream.h"

void MorrisLecar(hls::stream<stream_t> &Iext, hls::stream<stream_t> &V_out,
                 data_t *V, data_t *W, parameters *params) {
#pragma HLS INTERFACE axis port = Iext
#pragma HLS INTERFACE axis port = V_out
#pragma HLS INTERFACE s_axilite port = return
#ifdef LUT
#pragma HLS ARRAY_PARTITION variable = tanh_LUT dim = 1
#pragma HLS ARRAY_PARTITION variable = sech_LUT dim = 1
#endif

  stream_t temp;
  converter_t converter;
  while (!Iext.empty()) {
    Iext.read(temp);
    converter.i = temp.data;
    data_t Iinj = converter.f;
    // data_t IL = leakage_current(*V);
    // data_t INa = Na_current(*V);
    // data_t IK = Ka_current(*V, *W);
    // data_t Winf = winf(*V);
    // data_t tau = tauw(*V);
    // data_t diffv = dvdt(Iinj, IL, INa, IK);
    // data_t diffw = dwdt(Winf, tau, *W);

    data_t IL = params->g_leak * (*V - params->el_m);
    data_t minf =
        0.5 * (1 + hls::tanh((*V - params->beta_m) / params->gamma_m));
    data_t winf =
        0.5 * (1 + hls::tanh((*V - params->beta_w) / params->gamma_w));
    data_t tauw = 1 / hls::cosh(0.5 * (*V - params->beta_w) / params->gamma_w);
    data_t INa = params->g_fast * minf * (*V - params->eNa_m);
    data_t IK = params->g_slow * *W * (*V - params->ek_m);
    data_t dvdt = (Iinj - IL - INa - IK) / params->cm_m;
    data_t dwdt = (winf - *W) * params->phi / tauw;

    *V += dvdt * params->dt;
    *W += dwdt * params->dt;
    converter.f = *V;
    temp.data = converter.i;
    V_out.write(temp);
  }
}

// data_t leakage_current(data_t V) { return g_leak * (V - el_m); }

// data_t Na_current(data_t V) { return g_fast * minf(V) * (V - eNa_m); }

// data_t minf(data_t V) {
// #ifdef LUT
//   return (data_t)0.5 * ((data_t)1 + tanh_apr((V - beta_m) / gamma_m));
// #else
//   return (data_t)0.5 * ((data_t)1 + hls::tanh((V - beta_m) / gamma_m));
// #endif
// }

// data_t Ka_current(data_t V, data_t W) { return g_slow * W * (V - ek_m); }

// data_t tauw(data_t V) {
// #ifdef LUT
//   return sech_apr(0.5 * (V - beta_w) / gamma_w);
// #else
//   return 1 / hls::cosh(0.5 * (V - beta_w) / gamma_w);
// #endif
// }

// data_t winf(data_t V) {
// #ifdef LUT
//   return (data_t)0.5 * ((data_t)1 + tanh_apr((V - beta_w) / gamma_w));
// #else
//   return (data_t)0.5 * ((data_t)1 + hls::tanh((V - beta_w) / gamma_w));
// #endif  // LUT
// }

// data_t dvdt(data_t Iext, data_t Il, data_t INa, data_t IK) {
//   return (Iext - Il - INa - IK) / cm_m;
// }

// data_t dwdt(data_t Winf, data_t tauw, data_t W) {
//   return (Winf - W) * phi / tauw;
// }
// #ifdef LUT
// data_t tanh_apr(data_t x) {
//   data_t ret = 1;
//   if (hls::abs(x) < 3)
//     ret = (x > 0) ? tanh_LUT[(int)x * 256] : -tanh_LUT[(int)x * 256];
//   if (x < 0) ret = ret * -1;
//   return ret;
// }

// data_t sech_apr(data_t x) {
//   data_t ret = 0;
//   if (hls::abs(x) < 6)
//     ret = (x > 0) ? sech_LUT[(int)x * 256] : -sech_LUT[(int)x * 256];
//   if (x < 0) ret = ret * -1;
//   return ret;
// }
// #endif  // LUT