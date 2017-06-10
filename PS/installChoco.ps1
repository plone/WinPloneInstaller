if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }

Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy unrestricted -Force
iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex
Set-ItemProperty HKCU:\Software\PloneInstaller install_status "choco_installed"