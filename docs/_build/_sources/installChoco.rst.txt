.. _installchoco:

installChoco.ps1
================

This is the first PowerShell script called when installing on a machine that cannot run WSL, or the user opted out of WSL. It installs :ref:`chocolatey` on the user's machine. PowerShell must be restarted for this installation to take effect.

This script is isolated because a new instance of PowerShell must be opened before we can use Chocolatey to install dependencies.

:ref:`installplonebuildout` is called next.