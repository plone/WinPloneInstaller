#
# enableWSL.ps1
#
#If (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
#{
#	Start-Process powershell -Verb runAs
#	Break
#}
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }


if ((Get-WmiObject win32_operatingsystem).buildNumber -ge 15063) 
{
	reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock" /t REG_DWORD /f /v "AllowDevelopmentWithoutDevLicense" /d "1"
	if (Invoke-Elevated (Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq "Enabled")
	{
		if (Get-Command bash -ErrorAction SilentlyContinue){exit 2}
		else {powershell .\installWSL}
	}
	else 
	{
		Enable-WindowsOptionalFeature -Online  -NoRestart -FeatureName Microsoft-Windows-Subsystem-Linux
		Push-Location
		Set-Location HKCU:\Software\PLONE
		Set-ItemProperty . install_status "wsl_enabled"
		Pop-Location
		"Windows Subsystem for Linux Enabled" | Add-Content 'installLog.txt'
		Restart-Computer
	}
}
else {exit 1} 
#exit 1 - not a high enough build number to run this script
#exit 2 - WSL is already installed and run .. will not override current setup please remove bash shell before continueing