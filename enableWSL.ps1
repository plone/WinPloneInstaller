#
# enableWSL.ps1
#
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
		New-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce" -Force | Out-Null
		$value = "Powershell " + (Resolve-Path .\).Path + "\installWSL"
		New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce" -name MyKey -propertytype String -value $value
	}
}
else {exit 1} 
#exit 1 - not a high enough build number to run this script
#exit 2 - WSL is already installed and run .. will not override current setup please remove bash shell before continueing