launch.sh
=========
luanch.sh is a bash script we call inside `WSL <https://github.com/plone/WinPloneInstaller/wiki/WSL>`_.
It takes the name of another script as a parameter, and launches that script as a super user/root.
This was found to be much more reliable than placing sudo before respective commands.