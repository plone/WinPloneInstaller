.. _winploneinstaller:

WinPloneInstaller.py
====================

WinPloneInstaller.py contains the main logic of the installer. `PyInstaller <https://github.com/lucid-0/WinPloneInstaller/wiki/PyInstaller>`_ is used to convert this file to an executable that includes its dependencies. There are plenty of comments inside the file to help understand what it is doing, but the basic strategy is:

* Check if our Windows registry key already exists.

  * If so, read it in and call the appropriate function to continue installation.
  * If not, initialize it to "begin" and display the GUI
   
*  User selects Linux Subsystem or Standard Buildout installation

  * If Linux Subsystem is chosen and user has up to date Windows 10:

    * Enable and install the Windows Subsystem for Linux
    * Run bash script which retrieves and runs the universal installer

  * If Standard Buildout is chosen

    * Install `Chocolatey <https://github.com/lucid-0/WinPloneInstaller/wiki/chocolatey>`_ (a software manager for Windows)
    * Use to install Python, Git, etc.
    * Run buildout

The process is generally to call out (to PowerShell for example) for an action, and then wait for the Windows registry to reflect progress. wait_for_status_change(timeout) function takes an integer and allows that many attempts in reading the registry for status updates. There is a 2 second pause in the registry query code to prevent an overflow of registry reads, so currently a timeout value of 15 attempts will leave around 30 seconds for the external process to complete. wait_for_status_change(timeout) is generally called after each call to run_PS(scriptName) 