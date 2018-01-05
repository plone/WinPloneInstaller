Windows Subsystem for Linux
===========================

Since the Anniversary Update, there has been a Linux subsystem available for Windows 10. Since we have a nice Linux-based universal installer for Plone, this subsystem is an easy route to a Windows instance of Plone.

`check_wsl.ps1 <https://github.com/plone/WinPloneInstaller/wiki/check_wsl.ps1>`_ and `install_wsl.ps1 <https://github.com/plone/WinPloneInstaller/wiki/install_wsl.ps1>`_ are PowerShell scripts dealing with getting WSL on the user's machine, and `plone.sh <https://github.com/plone/WinPloneInstaller/wiki/plone.sh>`_ is a Bash script which is called within WSL after it is installed.

Check out Microsoft's overview of WSL `here <https://msdn.microsoft.com/en-us/commandline/wsl/about>`_.