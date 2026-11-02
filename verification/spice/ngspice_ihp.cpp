// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <ngspice/sharedspice.h>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

namespace {
bool failed = false;
int output(char* text, int, void*) { std::cerr << text << '\n'; return 0; }
int on_exit(int, NG_BOOL, NG_BOOL, int, void*) { failed = true; return 0; }
}

int main(int argc, char** argv) {
  if (argc != 2) { std::cerr << "usage: ngspice_ihp path/to/cornerHBT.lib\n"; return 2; }
  if (ngSpice_Init(output, nullptr, on_exit, nullptr, nullptr, nullptr, nullptr)) return 3;
  std::vector<std::string> lines = {
      "HeaviSolve IHP npn13G2 DC smoke test",
      ".lib \"" + std::string(argv[1]) + "\" hbt_typ",
      "Vc c 0 1.0", "Vb b 0 0.8", "Xq c b 0 0 npn13G2", ".op", ".end"};
  std::vector<char*> deck;
  for (auto& line : lines) deck.push_back(line.data());
  deck.push_back(nullptr);
  if (ngSpice_Circ(deck.data())) return 4;
  char run[] = "run";
  if (ngSpice_Command(run) || failed) return 5;
  char name[] = "vc#branch";
  auto* current = ngGet_Vec_Info(name);
  if (!current || current->v_length != 1 || !std::isfinite(current->v_realdata[0])) return 6;
  const double collector = -current->v_realdata[0];
  std::cout << std::setprecision(17) << "device=npn13G2 vce_v=1 vbe_v=0.8 collector_current_a="
            << collector << " status=" << (collector > 0 ? "PASS_SMOKE_ONLY" : "FAIL") << '\n';
  return collector > 0 ? 0 : 1;
}
