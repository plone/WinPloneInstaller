get_build_number.ps1
====================

This is a short PowerShell script called while the installer is initializing. It stores the Windows build number in the registry so WinPloneInstaller.py knows whether to take the WSL or Buildout intallation path.