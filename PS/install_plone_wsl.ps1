$host.ui.RawUI.WindowTitle = “Installing Plone on WSL”
$ploneKey = 'HKCU:\Software\PloneInstaller'
$plonePath = (Get-ItemProperty -Path $ploneKey -Name base_path).base_path
Set-Location $plonePath
. ".\PS\log.ps1"
#log("Downloading the Plone Unified Installer")
#(New-Object Net.WebClient).DownloadFile("https://launchpad.net/plone/5.0/5.0.7/+download/Plone-5.0.7-UnifiedInstaller.tgz", "$plonePath\PloneUnified.tgz")
log("Calling WinPloneInstaller bash script")
bash -c "./bash/plone.sh"
Write-Host -NoNewLine "debug"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")