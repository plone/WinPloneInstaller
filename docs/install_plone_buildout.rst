install_plone_buildout.ps1
========================

This is the second and final PowerShell script called when installing on a machine that cannot run `WSL <https://github.com/lucid-0/WinPloneInstaller/wiki/WSL>`_, or the user opted out of WSL (preceded by `install_choco.ps1 <https://github.com/lucid-0/WinPloneInstaller/wiki/install_choco.ps1>`_).

This script configures the newly installed `Chocolatey <https://github.com/lucid-0/WinPloneInstaller/wiki/Chocolatey>`_ and uses it to download Python, Git, and the VC++ tools for Python (Plone/Buildout dependencies).

It sets up virtualenv, clones `Plone's buildout repo from GitHub <https://github.com/plone/simple-plone-buildout>`_, and installs Plone using this `Buildout <https://github.com/lucid-0/WinPloneInstaller/wiki/Buildout>`_ method.