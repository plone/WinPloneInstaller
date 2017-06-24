$ploneKey = 'HKCU:\Software\PloneInstaller'
$tempPath = (Get-ItemProperty -Path $ploneKey -Name base_path).base_path
Set-Location $tempPath
echo "**Calling plone.sh in bash"
bash -c "./bash/plone.sh"
echo "*!Plone Installation Complete"