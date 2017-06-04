if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock" /t REG_DWORD /f /v "AllowDevelopmentWithoutDevLicense" /d "1"
if ((Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq "Enabled") {
	if (Get-Command bash -ErrorAction SilentlyContinue) { # WSL is already installed...will not override current setup, just run plone.sh
		Set-ItemProperty HKCU:\Software\PloneInstaller install_status "wsl_installed"
		"Windows Subsystem for Linux Enabled" | Add-Content 'installLog.txt'
	} else { #WinPloneInstaller.py will call installPlone.ps1
		Set-ItemProperty HKCU:\Software\PloneInstaller install_status "wsl_enabled"
		"Windows Subsystem for Linux Enabled" | Add-Content 'installLog.txt'

		Write-Host "Press any key to continue ..."
		$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
		Write-Host
		Write-Host "A"
		Write-Host "B"
		Write-Host "C"

		Restart-Computer

		Write-Host "Press any key to continue ..."
		$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
		Write-Host
		Write-Host "A"
		Write-Host "B"
		Write-Host "C"
	}
} else {
	Enable-WindowsOptionalFeature -Online  -NoRestart -FeatureName Microsoft-Windows-Subsystem-Linux
	Set-ItemProperty HKCU:\Software\PloneInstaller install_status "wsl_enabled"
	"Windows Subsystem for Linux Enabled" | Add-Content 'installLog.txt'
}