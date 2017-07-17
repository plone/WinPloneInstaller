WinPloneInstaller.py
====================

WinPloneInstaller.py contains the main logic of the installer. `PyInstaller <https://github.com/lucid-0/WinPloneInstaller/wiki/PyInstaller>`_ is used to convert this file to an executable that includes its dependencies.

See the name and description of each function as they appear in the WinPloneInstaller class below.

There are plenty of comments inside the file to help understand what it is doing, but the basic strategy is:

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

Function listing
================
__init__()
----------
This is of course called when an instance of WinPloneInstaller is created. 
Open or create the PloneInstaller registry key and make sure registry values for the executable path and its working path in Windows temporary directory are set.
Call get_build_number()
Call init_GUI()

get_build_number()
------------------
Simply runs get_build_number.ps1 in PowerShell, which sets a build_number registry value, and pulls that value into Python.
This is done this way to avoid unreliable results we got when using Python itself to get the build number (e.g. with the os, sys, or platform modules)

init_GUI()
----------
This is our main Tkinter set up. Creates a gui object, populates a frame with the log text, progress bar, checkboxes and buttons and places the frame in the gui object.
There is also a bit of code here to check if this machine has a high enough build number for WSL. If not, remove the WSL-specific options from the GUI and log a message about updating.

okay_handler(event)
-------------------
The okay button is bound to this function.
Disables the okay button because there is never a point where it should be clicked twice in a row.
Calls set_reg_vars to get the users configuration in the registry
If the installer is in a normal state, it calls init_install(). If it is waiting for

cancel_handler(event)
---------------------
The cancel button is bound to this function.
See kill_app()

init_install()
--------------
Compare machine build number to the required build number.
Call install_plone_buildout() or install_plone_wsl() accordingly.

install_plone_buildout()
------------------------

check_wsl()
-----------

enable_wsl()
------------

install_wsl()
-------------

install_plone_wsl()
-------------------

update_bash_script()
--------------------

set_reg_vars()
--------------
Put the user's installation configuration in the registry, in case we have to restart the machine or the installer.

get_reg_vars()
--------------
Get the user's installation configuration from the registry, if it exists.

run_PS(script_name, pipe=True, hide=True)
-----------------------------------------
Run one of the bundles scripts in PowerShell. script_name is the name of a file in the \PS folder of the installer's working directory in Windows temporary files.
If hide is true, the PowerShell window will be hidden.
If pipe is true, the output of PowerShell will be piped back into the Python terminal.
If the user must interact with the powershell script, both pipe and hide should be false. This will hide the installer GUI and show only the PowerShell window until it finishes and the GUI returns to focus.
2 asterisks (**) at the beginning of an echoed message from a piped PowerShell script will be logged in Python and shown to the user.
An asterisk and an exclamation (*!) at the beginning of an echoed message from a piped PowerShell script will be logged in Python as well as causing a call to PS_status_handler where the echoed message will cause a change in Python control flow.

PS_status_handler(status)
-------------------------
As mentioned in run_PS description above, an asterisk and an exclamation (*!) at the beginning of an echoed message from a piped PowerShell script will be logged in Python as well as causing a call to PS_status_handler where the echoed message will cause a change in Python control flow.
This function is used when PowerShell code determines what happens next in the Python.
For example "*!Installing WSL" appears in enable_wsl.ps1 when PowerShell determines that WSL is enabled but not yet installed. Python recieves this piped message and calls run_PS("install_wsl.ps1").

log(message, display=True)
--------------------------

restart_computer()
------------------

run_plone()
-----------

clean_up()
----------

kill_app()
----------