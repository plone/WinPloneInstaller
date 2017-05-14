#
# installPloneBuildout.ps1
#
If (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
	$arguments = "& '" + $myinvocation.mycommand.definition + "'"
	Start-Process powershell -Verb runAs -ArgumentList $arguments
	Break
}

choco install vcpython27
choco install git
choco install python2

"Installed Plone Dependencies using Chocolatey" | Add-Content 'installLog.txt'
Set-Location HKCU:\Software\PLONE
Set-ItemProperty . install_status "dependencies_installed"

pip install virtualenv
git clone https://github.com/plone/simple-plone-buildout
cd simple-plone-buildout
copy profiles\buildout.cfg.tmpl buildout.cfg
virtualenv env
env\Scripts\pip install -r requirements.txt
env\Scripts\buildout
bin\instance start