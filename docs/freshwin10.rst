.. _freshwin10:

freshwin10.ps1
=========

This PowerShell script simply uninstalls and disables WSL. It is just here for convenience when testing the installer. The contents of freshwin10.ps1 are below::

  lxrun /uninstall /full
  Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux