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

#Below will be elevated
$requiredBuild = 15063
$buildNumber = [int](Get-WmiObject win32_operatingsystem).buildNumber
if ($buildNumber -lt $requiredBuild) {
    echo "**This system has Windows build number " + $buildNumber + "."
    echo "**Windows 10 with Creator's Update (build 15063) required to install on WSL (recommended)"
    echo "*!Installing Plone with buildout"
    Set-ItemProperty HKCU:\Software\PloneInstaller install_status "install_with_buildout" #This is not high enough Windows build.
} else {
    echo "**Plone can be installed on WSL (recommended) on this system!"
    reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock" /t REG_DWORD /f /v "AllowDevelopmentWithoutDevLicense" /d "1"
    if ((Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq "Enabled") {
        if (Get-Command bash -ErrorAction SilentlyContinue) { # WSL is already installed...will not override current setup, WinPloneInstaller will call install_wsl.ps1
            echo "**WSL is installed on this machine"
            echo "*!Installing Plone on WSL"
        } else { #WinPloneInstaller.py will call install_wsl.ps1
            echo "**WSL is enabled on this machine"
            echo "*!Installing WSL"
        }
    } else { #WinPloneInstaller.py will complete this code block
        echo "**Enabling WSL. Please allow PowerShell to"
        echo "*!restart the machine"
        Set-ItemProperty HKCU:\Software\PloneInstaller install_status "enabling_wsl"
        
        Enable-WindowsOptionalFeature -Online -NoRestart -FeatureName Microsoft-Windows-Subsystem-Linux