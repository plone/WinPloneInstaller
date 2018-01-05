build.ps1
=========

This PowerShell script simply calls `PyInstaller <https://github.com/plone/WinPloneInstaller/wiki/PyInstaller>`_ with the parameters and options we need to build WinPloneInstaller into a Windows executable. It is just here for convenience when developing the installer. The contents of build.ps1 are below::

  pyinstaller --add-data './PS/*;./PS' --add-data './bash/*;./bash' --onefile --windowed --icon=./resources/plone.ico -F WinPloneInstaller.py