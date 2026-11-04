// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <N_CIR_XyceCInterface.h>
#include <algorithm>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <numbers>

int main(int argc, char** argv) {
  if (argc != 3) { std::cerr << "usage: xyce_step circuit.cir output.csv\n"; return 2; }
  void* simulator = nullptr;
  xyce_open(&simulator);
  if (!simulator) return 3;
  char name[] = "Xyce";
  char* args[] = {name, argv[1]};
  if (xyce_initialize(&simulator, 2, args) != 1) {
    xyce_close(&simulator); return 4;
  }
  std::ofstream output(argv[2]);
  output << "requested_s,completed_s,voltage_v,analytic_v,absolute_error_v\n" << std::setprecision(17);
  constexpr double tau = 1e-6;
  constexpr double omega = 2 * std::numbers::pi * 1e6;
  double maximum = 0, previous = 0;
  bool passed = true;
  char voltage[] = "V(out)";
  for (int step = 1; step <= 50; ++step) {
    const double requested = step * 1e-7;
    double completed = 0;
    const int status = xyce_simulateUntil(&simulator, requested, &completed);
    const double value = xyce_getCircuitValue(&simulator, voltage);
    const double exact = (std::sin(omega * completed) - omega * tau * std::cos(omega * completed)
                        + omega * tau * std::exp(-completed / tau)) / (1 + omega * omega * tau * tau);
    const double error = std::abs(value - exact);
    passed = passed && status == 1 && std::isfinite(value) && std::isfinite(completed)
             && completed > previous && std::abs(completed - requested) <= 1e-12 && error <= 1e-4;
    maximum = std::max(maximum, error);
    output << requested << ',' << completed << ',' << value << ',' << exact << ',' << error << '\n';
    previous = completed;
  }
  passed = passed && output.good();
  xyce_close(&simulator);
  std::cout << std::setprecision(17) << "steps=50 max_absolute_error_v=" << maximum
            << " tolerance_v=0.0001 status=" << (passed ? "PASS" : "FAIL") << '\n';
  return passed ? 0 : 1;
}
