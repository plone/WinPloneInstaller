install_choco.ps1
================

This is the first PowerShell script called when installing on a machine that cannot run `WSL <https://github.com/lucid-0/WinPloneInstaller/wiki/WSL>`_, or the user opted out of WSL.

`Chocolatey <https://github.com/lucid-0/WinPloneInstaller/wiki/Chocolatey>`_ provides a PowerShell script that can be invoked over the web to install it on the user's machine. PowerShell must be restarted for this installation to take effect.

This script is isolated because a new instance of PowerShell must be opened before we can use Chocolatey to install dependencies.

`install_plone_buildout.ps1 <https://github.com/lucid-0/WinPloneInstaller/wiki/install_plone_buildout.ps1>`_ is called next.