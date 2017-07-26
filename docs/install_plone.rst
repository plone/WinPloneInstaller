install_plone.sh
================
install_plone.sh is a bash script we call inside `WSL <https://github.com/lucid-0/WinPloneInstaller/wiki/WSL>`_. It performs the following:
* Switch to super user
* Update/Upgrade the new instance of WSL (this adds quite a long time to installation, may be better to just make sure a few necessary tools are up to date)
* Install some depencies for Plone
* Download and extract the Plone Universal Installer
* Start the universal installer with options selected in `WinPloneInstaller's <https://github.com/lucid-0/WinPloneInstaller/wiki/WinPloneInstaller.py>`_ GUI.

Some crucial lines of this script are actually "missing" as they are bundled in the executable. These lines are added by WinPloneInstaller's update_bash_script() function to allow installation configuration.