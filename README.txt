Steps for creating installer EXE with PyInstaller
	Get python
	Make sure pip is installed and accessible from powershell
	Run "pip install pyinstaller" in powershell
	Install python-tk package for GUI
	Run "pyinstaller --add-data './*.ps1;./PS' -F WinPloneInstaller.py" in powershell (need to add plone.sh to this line)