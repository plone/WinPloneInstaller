# Project Build Debugging Suggestions

When building the Windows Plone Installer there are some things to keep in mind.

 - Build on Win10 for Win10! PyInstaller acts differently on different platforms. Our main goal is to build a Windows 10 Application and our best bet is to build on  Windows 10 running Python 3.5
 - Any error outputs from PyInstaller that seem to be involved with your Python code can be addressed more directly by trying to run the script directly in Python.
 - The Windows registry effects the environment! If you are having trouble building, try deleting the PloneInstaller key using regedit and see if you get a different result.
  - Remove "--windowed" from build.ps1 to see the Python shell's output for WinPyInstaller.py when running WinPyInstaller.exe, replace "--windowed" to maintain a more user friendly view in the end product.