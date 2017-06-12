if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }

choco feature enable -n=allowGlobalConfirmation
choco feature enable -n=virusCheck
choco feature enable -n=allowEmptyChecksums
choco install pscx

choco install vcpython27
choco install git
choco install python2
pip install virtualenv

Set-ItemProperty HKCU:\Software\PloneInstaller install_status "dependencies_installed"

git clone https://github.com/plone/simple-plone-buildout
cd simple-plone-buildout
copy profiles\buildout.cfg.tmpl buildout.cfg
virtualenv env
env\Scripts\pip install -r requirements.txt
Set-ItemProperty HKCU:\Software\PloneInstaller install_status "starting_buildout"
env\Scripts\buildout
bin\instance start