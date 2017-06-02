Steps for creating installer EXE with PyInstaller
	Get python (currently building on 2.7)
	Make sure pip is installed and accessible from powershell
	Run "pip install pyinstaller"
	Be sure python-tk package is installed for GUI (hit and miss for me whether I had to do this manually)
	Run build.ps1 in powershell

To test the project on Win10 you might want to be able to uninstall
WSL in order to start with a "clean" environment. Just run freshwin10.ps1
in PowerShell to do so.