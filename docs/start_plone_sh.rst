start_plone.sh
==============
start_plone.sh is a bash script we call inside `WSL <https://github.com/lucid-0/WinPloneInstaller/wiki/WSL>`_ after installation has completed.
It simply starts Plone using::

  sudo -u plone_daemon /etc/Plone/zinstance/bin/plonectl fg