freshwin10.ps1
==============

This PowerShell script simply uninstalls and disables `WSL <https://github.com/lucid-0/WinPloneInstaller/wiki/WSL>`_. It is just here for convenience when testing the installer. The contents of freshwin10.ps1 are below::

  lxrun /uninstall /full
  Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux