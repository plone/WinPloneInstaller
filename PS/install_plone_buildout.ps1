$host.ui.RawUI.WindowTitle = "Installing Plone with Buildout"
$ploneKey = 'HKCU:\Software\PloneInstaller'
$plonePath = (Get-ItemProperty -Path $ploneKey -Name base_path).base_path
$installDirectory = (Get-ItemProperty -Path $ploneKey -Name install_directory).install_directory
. "$plonePath\PS\log.ps1"

log("Configuring Chocolatey")
choco feature enable -n=allowGlobalConfirmation
choco feature enable -n=virusCheck
choco feature enable -n=allowEmptyChecksums

log("Installing pscx")
choco install pscx -y
log("Installing MS VC++ Compiler for Python 2.7")
choco install vcpython27 -y
log("Installing git")
choco install git -y
log("Installing Python 2.7")
choco install python2 --force

$env:Path += ";C:\python27\Scripts;C:\python27;C:\Program Files\Git\bin;C:\Program Files (x86)\Git\bin"
log("Installing virtualenv")
pip install virtualenv

log("Cloning simple-plone-buildout")

Set-Location $installDirectory
git clone https://github.com/plone/simple-plone-buildout
Rename-Item simple-plone-buildout Plone
Set-Location Plone
Copy-Item profiles\buildout.cfg.tmpl buildout.cfg
virtualenv -p C:\python27\python.exe env
env\Scripts\pip install -r requirements.txt
log("Starting buildout, this will take a while...")
env\Scripts\buildout
log("Plone Installed Successfully")
Write-Host -NoNewLine "Press any key and the Plone installer will clean up and finish."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
