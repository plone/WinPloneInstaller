if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }

choco install vcpython27
choco install git
choco install python2

"Installed Plone Dependencies using Chocolatey" | Add-Content 'installLog.txt'
Set-ItemProperty HKCU:\Software\Plone install_status "dependencies_installed"

pip install virtualenv
git clone https://github.com/plone/simple-plone-buildout
cd simple-plone-buildout
copy profiles\buildout.cfg.tmpl buildout.cfg
virtualenv env
env\Scripts\pip install -r requirements.txt
env\Scripts\buildout
bin\instance start