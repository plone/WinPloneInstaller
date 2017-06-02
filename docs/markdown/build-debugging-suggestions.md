# Project Build Debugging Suggestions

When building the Windows Plone Installer there are some things to keep in mind.

 - Any error outputs from PyInstaller that seem to be involved with your Python code can be addressed more directly by trying to run the script directly in Python.
 - The Windows registry effects the environment! If you are having trouble building, try deleting the PloneInstaller key using regedit and see if you get a different result.