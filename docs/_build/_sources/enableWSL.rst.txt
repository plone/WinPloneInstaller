.. _enablewsl:

EnableWSL.ps1
=============

This is the first PowerShell script the installer will run on machines which will utilize :ref:`wsl`.

WSL is an optional Windows feature, if it was disabled at the beginning of this script we must enable it and restart the machine and run :ref:`installwsl` to install it.
If already installed, we jump right into installing Plone on it using :ref:`plone-bash`.