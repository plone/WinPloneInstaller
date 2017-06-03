# installChoco.ps1

This is the first PowerShell script called when installing on a machine that cannot run WSL, or the user opted out of WSL. It installs [Chocolatey](chocolatey.html) on the user's machine. PowerShell must be restarted for this installation to take effect.

[installPloneBuildout.ps1](installPloneBuildout.html) is called next.