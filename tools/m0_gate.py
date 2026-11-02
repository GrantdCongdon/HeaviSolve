# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Never turn partial numerical diagnostics into an M0 completion claim."""
import pathlib
import sys
import tomllib
path=pathlib.Path(__file__).resolve().parents[1]/'verification/m0-status.toml'
status=tomllib.loads(path.read_text())
missing=[key for key,value in status['gate'].items() if value is not True]
if missing:
    print('M0 NOT COMPLETE: '+', '.join(missing));sys.exit(1)
print('M0 gates marked complete; review linked CI evidence before release')
