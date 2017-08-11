Project Debugging Suggestions
=============================

When building the Windows Plone Installer there are some things to keep in mind.

* PyInstaller acts differently on different platforms. Our main goal is to build a Windows application and our best bet is to build on Windows running Python 3.5. Since the Windows 7 build also runs on 8 and 10, it is preferred to build on Windows 7.
* Any error outputs from PyInstaller that seem to be involved with your Python code can be addressed more directly by trying to run the script directly in Python. Be careful here though; function calls in WinPyInstaller.py might end up modifying project scripts this way! (this kind of test should be done in a backup copy of the project)
* The Windows registry effects the environment! If you are having trouble building, try deleting the PloneInstaller key using regedit and see if you get a different result.
* Remove "--windowed" from build.ps1 to see the Python shell's output for WinPyInstaller.py when running WinPyInstaller.exe, replace "--windowed" to maintain a more user friendly view in the end product.

If you have unexplained trouble with plone.sh, ensure that it didn't end up with Windows line ending characters (as opposed to Unix line endings). If nothing else appears wrong with the script, try converting to unix-style line endings (many editors and tools allow this)