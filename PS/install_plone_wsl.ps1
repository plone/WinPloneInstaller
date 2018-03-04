$host.ui.RawUI.WindowTitle = "Installing Plone on WSL"
$ploneKey = 'HKCU:\Software\PloneInstaller'
$plonePath = (Get-ItemProperty -Path $ploneKey -Name base_path).base_path
Set-Location $plonePath
. ".\PS\log.ps1"
Set-Location bash
log("Calling Plone installation script in Bash")
$bash = $(Start-Process -FilePath "bash" -ArgumentList ("-c","./launch.sh\ install_plone") -PassThru);
$bash | Wait-Process;
