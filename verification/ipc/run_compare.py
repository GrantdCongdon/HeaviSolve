# SPDX-FileCopyrightText: 2026 HeaviSolve contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Launch independent native processes and retain their local IPC measurements."""
import pathlib
import select
import subprocess
import tempfile
ROOT=pathlib.Path(__file__).resolve().parents[2]
binary=ROOT/'.work/ipc-build/ipc_compare'
for protocol in ('grpc','zmq'):
    with tempfile.TemporaryDirectory(prefix='heavisolve-ipc-',dir='/tmp') as tmp:
        endpoint=tmp+'/control';data=tmp+'/array'
        server=subprocess.Popen([str(binary),'server',protocol,endpoint,data],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        try:
            readable,_,_=select.select([server.stdout],[],[],30)
            if not readable or server.stdout.readline().strip()!='READY':
                raise RuntimeError('Server failed to become ready')
            client=subprocess.run([str(binary),'client',protocol,endpoint,data],capture_output=True,text=True,timeout=40)
            print(client.stdout,end='')
            if client.returncode:
                raise RuntimeError(client.stderr)
        finally:
            if server.poll() is None:server.terminate()
            try:server.wait(timeout=5)
            except subprocess.TimeoutExpired:server.kill();server.wait()
