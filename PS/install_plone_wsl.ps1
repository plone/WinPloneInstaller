$host.ui.RawUI.WindowTitle = "Installing Plone on WSL"
$ploneKey = 'HKCU:\Software\PloneInstaller'
$plonePath = (Get-ItemProperty -Path $ploneKey -Name base_path).base_path
Set-Location $plonePath
. ".\PS\log.ps1"
log("Calling WinPloneInstaller bash script")
bash -c "./bash/plone.sh"
Write-Host -NoNewLine "Press any key and WinPloneInstaller will clean up and finish."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")