get_win_info.ps1
==============

In testing earlier versions of the installer, it was discovered that PowerShell is more reliable than Python at determining which Windows build number the script is being executed on (which comes as no surprise).

This script is the first thing called on the installation machine, it places the Windows version number in the registry so `WinPloneInstaller.py <https://github.com/lucid-0/WinPloneInstaller/wiki/WinPloneInstaller.py>`_ can determine which options to allow the user and whether to install using `WSL <https://github.com/lucid-0/WinPloneInstaller/wiki/WSL>`_ or `Buildout <https://github.com/lucid-0/WinPloneInstaller/wiki/Buildout>`_