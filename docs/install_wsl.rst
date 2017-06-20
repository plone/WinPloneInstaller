install_wsl.ps1
==============

This is the second PowerShell script the installer will run on machines which will utilize `WSL <https://github.com/lucid-0/WinPloneInstaller/wiki/WSL>`_.

Preceded by `enabled_wsl.ps1 <https://github.com/lucid-0/WinPloneInstaller/wiki/enabled_wsl.ps1>`_.

It simply calls lxrun (Windows 10's Linux Subsystem downloader and installer) and updates the install_status variable in the registry.