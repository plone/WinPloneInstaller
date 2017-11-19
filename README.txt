Plone Installer for Windows
===========================

The Plone installer for Windows will do one of two things:

- for Windows 10 and later: install the Windows Subsystem for Linux (WSL) then run the Plone unified installer
- for earlier Windows versions: install the requirements for then run the Plone simple buildout

The current executable for the Plone installer for Windows is available in https://github.com/plone/WinPloneInstaller/tree/master/dist

Please file bug reports in https://github.com/plone/WinPloneInstaller/issues

Development Notes
-----------------
Please see the github repo for documentation! It is in the wiki (https://github.com/lucid-0/WinPloneInstaller/wiki)
(a copy of the reStructuredText is also included in the /docs folder)

The project will be understood through WinPloneInstaller.py and its documentation, the WinPloneInstaller class within is certainly the "main" project code.

Steps for creating installer EXE with PyInstaller:
	Get python (currently building on 3.5.x)
	Make sure pip is installed and accessible from powershell
	Run "pip install pyinstaller"
	Run "pip install pillow"
	http://pywin32.sourceforge.net/ may need to be added manually (especially when building on older versions of Windows)
	Be sure python-tk package is installed for GUI (hit and miss for me whether I had to do this manually)
	Run build.ps1 in powershell

To test the project on Win10 you might want to be able to uninstall
WSL in order to start with a "clean" environment. Just run freshwin10.ps1
in PowerShell to do so.
