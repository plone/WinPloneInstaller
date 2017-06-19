plone.sh
========
plone.sh is a bash script we call inside `WSL <https://github.com/lucid-0/WinPloneInstaller/wiki/WSL>`_. It performs the following:
* Switch to super user
* Update/Upgrade the new instance of WSL (this adds quite a long time to installation, may be optional)
* Install some depencies for plone
* Download and extract the Plone Universal Installer
* Start the universal installer with options selected in `WinPloneInstaller's <https://github.com/lucid-0/WinPloneInstaller/wiki/WinPloneInstaller.py>`_ GUI.

Some crucial lines of this script are actually "missing" as they are bundled in the executable. These lines are added by WinPloneInstaller's update_scripts() function to allow installation configuration.