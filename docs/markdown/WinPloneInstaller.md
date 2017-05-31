# WinPloneInstaller.py

WinPloneInstaller.py contains the main logic of the installer. PyInstaller is used to convert this file to an executable that includes its dependencies. There are plenty of comments inside the file to help understand what it is doing, but the basic strategy is:

 - Check if our Windows registry key already exists.
    - If so, read it in and call the appropriate function to continue installation.
    - If not, initialize it to "begin" and display the GUI
   
 -  User selects Linux Subsystem or Standard Buildout installation
    - If Linux Subsystem is chosen and user has up to date Windows 10:
   	     - Enable and install the Windows Subsystem for Linux
         - Run bash script which retrieves and runs the universal installer
    - If Standard Buildout is chosen
        - Install Chocolately (a software manager for Windows)
        - Use Chololately to install Python, Git, etc.
        - Run buildout