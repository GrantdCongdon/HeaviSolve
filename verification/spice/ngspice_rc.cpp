// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <ngspice/sharedspice.h>
#include <algorithm>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>

namespace {
int callbacks = 0;
bool exited = false;
int output(char* text, int, void*) { std::cerr << text << '\n'; return 0; }
int on_exit(int, NG_BOOL, NG_BOOL, int, void*) { exited = true; return 0; }
int voltage(double* value, double, char*, int, void*) {
  ++callbacks;
  *value = 1.0;
  return 0;
}
}

int main(int argc, char** argv) {
  if (argc != 2) { std::cerr << "usage: ngspice_rc output.csv\n"; return 2; }
  if (ngSpice_Init(output, nullptr, on_exit, nullptr, nullptr, nullptr, nullptr)) return 3;
  int ident = 0;
  if (ngSpice_Init_Sync(voltage, nullptr, nullptr, &ident, nullptr)) return 4;
  char title[] = "HeaviSolve RC external-source spike";
  char source[] = "Vdrive in 0 external";
  char resistor[] = "R1 in out 1000";
  char capacitor[] = "C1 out 0 1n IC=0";
  char options[] = ".options reltol=1e-8 abstol=1e-12";
  char analysis[] = ".tran 1n 5u 0 1n uic";
  char end[] = ".end";
  char* circuit[] = {title, source, resistor, capacitor, options, analysis, end, nullptr};
  if (ngSpice_Circ(circuit)) return 5;
  char run[] = "run";
  if (ngSpice_Command(run) || exited) return 6;
  char time_name[] = "time";
  char voltage_name[] = "v(out)";
  auto* time_ptr = ngGet_Vec_Info(time_name);
  if (!time_ptr) return 7;
  const auto time_info = *time_ptr;
  const auto* time = &time_info;
  auto* volts = ngGet_Vec_Info(voltage_name);
  if (!time || !volts || time->v_length != volts->v_length || time->v_length < 100) return 7;
  std::ofstream file(argv[1]);
  file << "# SPDX-" "FileCopyrightText: 2026 HeaviSolve contributors\n"
          "# SPDX-" "License-Identifier: AGPL-3.0-or-later\n"
          "time_s,voltage_v,analytic_v,absolute_error_v\n";
  file << std::setprecision(17);
  double maximum = 0.0;
  for (int i = 0; i < time->v_length; ++i) {
    const auto t = time->v_realdata[i];
    const auto v = volts->v_realdata[i];
    const auto exact = -std::expm1(-t / 1e-6);
    if (!std::isfinite(t) || !std::isfinite(v)) return 8;
    const auto error = std::abs(v - exact);
    maximum = std::max(maximum, error);
    file << t << ',' << v << ',' << exact << ',' << error << '\n';
  }
  const bool passed = maximum <= 1e-4 && callbacks > 0 && file.good();
  std::cout << std::setprecision(17) << "samples=" << time->v_length
            << " external_source_callbacks=" << callbacks
            << " max_absolute_error_v=" << maximum
            << " tolerance_v=0.0001 status=" << (passed ? "PASS" : "FAIL") << '\n';
  return passed ? 0 : 1;
}
