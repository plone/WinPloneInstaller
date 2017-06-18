EnableWSL.ps1
=============

This is the first PowerShell script the installer will run on machines which will utilize `WSL <https://github.com/lucid-0/WinPloneInstaller/wiki/WSL>`_.

WSL is an optional Windows feature, if it was disabled at the beginning of this script we must enable it and restart the machine and run `installWSL.ps1 <https://github.com/lucid-0/WinPloneInstaller/wiki/installWSL.ps1>`_ to install it.
If already installed, we jump right into installing Plone on it by calling `plone.sh <https://github.com/lucid-0/WinPloneInstaller/wiki/plone.sh>`_.