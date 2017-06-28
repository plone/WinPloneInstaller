$ploneKey = 'HKCU:\Software\PloneInstaller'
$plonePath = (Get-ItemProperty -Path $ploneKey -Name base_path).base_path
Set-Location $plonePath
echo "**Downloading the Plone Unified Installer"
(New-Object Net.WebClient).DownloadFile("https://launchpad.net/plone/5.0/5.0.7/+download/Plone-5.0.7-UnifiedInstaller.tgz", "$plonePath\PloneUnified.tgz")
echo "**Calling WinPloneInstaller bash script"
bash -c "./bash/plone.sh"
echo "*!Plone Installed Successfully"