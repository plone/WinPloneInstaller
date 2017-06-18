Please see the github repo for documentation! It is in the wiki (https://github.com/lucid-0/WinPloneInstaller/wiki)
(a copy of the reStructuredText is also included in the /docs folder)

Steps for creating installer EXE with PyInstaller
	Get python (currently building on 3.5)
	Make sure pip is installed and accessible from powershell
	Run "pip install pyinstaller"
	Be sure python-tk package is installed for GUI (hit and miss for me whether I had to do this manually)
	Run build.ps1 in powershell

To test the project on Win10 you might want to be able to uninstall
WSL in order to start with a "clean" environment. Just run freshwin10.ps1
in PowerShell to do so.