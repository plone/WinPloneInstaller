if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock" /t REG_DWORD /f /v "AllowDevelopmentWithoutDevLicense" /d "1"
if ((Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq "Enabled") {
	if (Get-Command bash -ErrorAction SilentlyContinue) { # WSL is already installed...will not override current setup, just run plone.sh
		Push-Location
		Set-Location HKCU:\Software\Plone
		Set-ItemProperty . install_status "wsl_installed"
		Pop-Location
		"Windows Subsystem for Linux Enabled" | Add-Content 'installLog.txt'
	} else {
		Push-Location
		Set-Location HKCU:\Software\Plone
		Set-ItemProperty . install_status "wsl_enabled"
		Pop-Location
		"Windows Subsystem for Linux Enabled" | Add-Content 'installLog.txt'
	}
} else {
	Enable-WindowsOptionalFeature -Online  -NoRestart -FeatureName Microsoft-Windows-Subsystem-Linux

	Push-Location
	Set-Location HKCU:\Software\Plone
	Set-ItemProperty . install_status "wsl_enabled"
	Pop-Location
	"Windows Subsystem for Linux Enabled" | Add-Content 'installLog.txt'
}