#
# installPloneBuildout.ps1
#
If (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
	$arguments = "& '" + $myinvocation.mycommand.definition + "'"
	Start-Process powershell -Verb runAs -ArgumentList $arguments
	Break
}

pip install virtualenv
git clone https://github.com/plone/simple-plone-buildout
cd simple-plone-buildout
copy profiles\buildout.cfg.tmpl buildout.cfg
virtualenv env
env\Scripts\pip install -r requirements.txt
env\Scripts\buildout
bin\instance start