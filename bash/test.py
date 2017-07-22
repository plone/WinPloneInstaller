import os
import subprocess as sp
with open(os.devnull, 'r+b', 0) as DEVNULL:
    sp.Popen(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe",". ./test.ps1"], stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)