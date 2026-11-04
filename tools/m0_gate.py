# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Section12 M0 acceptance is distinct from deliverables and milestone exit."""
import argparse
import pathlib
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED = {
    'acceptance': ('language_slab_comparison', 'spice_measured_scoring',
                   'ci_stored_numerical_outputs', 'ci_license_scan_green'),
    'deliverables': ('phase_r_decisions_dispositioned', 'spike_reports_complete',
                     'repository_docs_and_standards', 'dependency_strategy_and_container'),
    'exit': ('adrs_accepted_and_merged', 'walking_skeleton_self_review'),
}
EVIDENCE = {
    'acceptance': ('docs/adr/ADR-001-language.md', 'docs/adr/ADR-003-spice-engine.md',
                   'docs/research/spice-engine-comparison.md',
                   'verification/results/ci-41668976621/provenance.json'),
    'deliverables': ('docs/research/solver-survey.md', 'docs/research/pdk-survey.md',
                     'docs/developer/dependencies.md', 'docs/developer/coding-standards.md',
                     'docs/adr/ADR-008-phase-r-component-dispositions.md',
                     'docker/Dockerfile', 'docs/research/name-availability.md'),
    'exit': ('docs/developer/walking-skeleton-plan.md', 'docs/milestones/M0-report.md'),
}

def missing_records(status, stages, root=ROOT):
    missing = []
    for stage in stages:
        for key in REQUIRED[stage]:
            if status.get(stage, {}).get(key) is not True:
                missing.append(stage + '.' + key)
        for name in EVIDENCE[stage]:
            if not (root / name).is_file():
                missing.append('missing evidence: ' + name)
    return missing

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=(*REQUIRED, 'all'), default='acceptance')
    args = parser.parse_args()
    status = tomllib.loads((ROOT / 'verification/m0-status.toml').read_text())
    stages = tuple(REQUIRED) if args.stage == 'all' else (args.stage,)
    missing = missing_records(status, stages)
    if missing:
        print('M0 ' + args.stage + ' NOT COMPLETE: ' + ', '.join(missing))
        return 1
    print('PASS: M0 ' + args.stage + ' records and evidence present. Numerical tests run separately.')
    if args.stage != 'all':
        print('This is not milestone completion; all deliverable and exit checks must also pass.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
