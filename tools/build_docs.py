# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Stage repository evidence into the documentation site without duplicating sources."""
import json
import pathlib
import shutil
import subprocess
import sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
stage=ROOT/'.work/docs-source'
shutil.rmtree(stage,ignore_errors=True)
shutil.copytree(ROOT/'docs',stage)
shutil.copytree(ROOT/'verification/results',stage/'results')
shutil.copy2(ROOT/'README.md',stage/'repository.md')
for page in stage.rglob('*.md'):
    text=page.read_text()
    text=text.replace('../../verification/results/','../results/')
    if page.name=='index.md': text=text.replace('../README.md','repository.md')
    if page.name=='repository.md':
        text=text.replace('docs/milestones/','milestones/').replace('[contribution rules](CONTRIBUTING.md)','contribution rules in the repository')
    page.write_text(text)
config=ROOT/'.work/docs-config.json'
config.write_text(json.dumps({'site_name':'HeaviSolve','docs_dir':str(stage),'site_dir':str(ROOT/'build/docs')}))
subprocess.run([sys.executable,'-m','mkdocs','build','--strict','--config-file',str(config)],check=True)
