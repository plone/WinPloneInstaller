if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }
$winVersion
Set-ItemProperty HKCU:\Software\Plone win_version (Get-CimInstance Win32_OperatingSystem).version
Set-ItemProperty HKCU:\Software\Plone install_status "got_win_info"
