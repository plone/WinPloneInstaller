if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }

if (Invoke-Elevated (Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq "Enabled") {
    Invoke-Elevated lxrun /install /y
    "Windows Subsystem for Linux Installed" | Add-Content 'C:\installLog.txt'
    Set-Location HKCU:\Software\Plone
    Set-ItemProperty . install_status "wsl_installed"
} else {exit 1}

#exit 1 - WSL is not enabled on this machine  