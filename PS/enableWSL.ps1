#Thank you Ben Armstrong for sharing this reliable script elevation strategy
#https://blogs.msdn.microsoft.com/virtual_pc_guy/2010/09/23/a-self-elevating-powershell-script/

# Get the ID and security principal of the current user account
$myWindowsID=[System.Security.Principal.WindowsIdentity]::GetCurrent()
$myWindowsPrincipal=new-object System.Security.Principal.WindowsPrincipal($myWindowsID)
 
# Get the security principal for the Administrator role
$adminRole=[System.Security.Principal.WindowsBuiltInRole]::Administrator
 
# Check to see if we are currently running "as Administrator"
if ($myWindowsPrincipal.IsInRole($adminRole)) {
   # We are running "as Administrator" - so change the title and background color to indicate this
   $Host.UI.RawUI.WindowTitle = $myInvocation.MyCommand.Definition + "(Elevated)"
   $Host.UI.RawUI.BackgroundColor = "DarkBlue"
   clear-host
} else {
   # We are not running "as Administrator" - so relaunch as administrator
   
   # Create a new process object that starts PowerShell
   $newProcess = new-object System.Diagnostics.ProcessStartInfo "PowerShell";
   
   # Specify the current script path and name as a parameter
   $newProcess.Arguments = $myInvocation.MyCommand.Definition;
   
   # Indicate that the process should be elevated
   $newProcess.Verb = "runas";
   
   # Start the new process
   [System.Diagnostics.Process]::Start($newProcess);
   
   # Exit from the current, unelevated, process
   exit
}

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock" /t REG_DWORD /f /v "AllowDevelopmentWithoutDevLicense" /d "1"
if ((Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq "Enabled") {
	if (Get-Command bash -ErrorAction SilentlyContinue) { # WSL is already installed...will not override current setup, WinPloneInstaller will call installWSL.ps1
		Set-ItemProperty HKCU:\Software\PloneInstaller install_status "wsl_installed"
	} else { #WinPloneInstaller.py will call installWSL.ps1
		Set-ItemProperty HKCU:\Software\PloneInstaller install_status "wsl_enabled"
	}
} else { #WinPloneInstaller.py will call restart.ps1
	Set-ItemProperty HKCU:\Software\PloneInstaller install_status "enabling_wsl"
    
	Enable-WindowsOptionalFeature -Online -NoRestart -FeatureName Microsoft-Windows-Subsystem-Linux
	Write-Host -NoNewLine "WinPloneInstaller needs to restart! It will continue when you return, press any key when ready..."
	$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
	Restart-Computer
}