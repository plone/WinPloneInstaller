$host.ui.RawUI.WindowTitle = "Installing Plone on WSL"
$ploneKey = 'HKCU:\Software\PloneInstaller'
$plonePath = (Get-ItemProperty -Path $ploneKey -Name base_path).base_path
Set-Location $plonePath
. ".\PS\log.ps1"
Set-Location bash
log("Calling WinPloneInstaller bash script")
bash -c "./launch.sh"
Write-Host -NoNewLine "Press any key and the Plone installer will clean up and finish."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")