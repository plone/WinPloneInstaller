#
# installChoco.ps1
#
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }

Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy unrestricted -Force
iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex
choco feature enable -n=allowGlobalConfirmation
choco feature enable -n=virusCheck
choco feature enable -n=allowEmptyChecksums
choco install pscx
"Installed Chocolatey" | Add-Content 'installLog.txt'
Set-Location HKCU:\Software\PLONE
Set-ItemProperty . install_status "choco_installed"