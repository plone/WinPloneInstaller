if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }

$ploneKey = 'HKCU:\Software\PloneInstaller'
$tempPath = (Get-ItemProperty -Path $ploneKey -Name base_path).base_path
Set-Location $tempPath
bash -c "./bash/plone.sh"
Set-ItemProperty HKCU:\Software\PloneInstaller install_status "complete"