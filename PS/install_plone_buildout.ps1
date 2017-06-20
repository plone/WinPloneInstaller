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
choco feature enable -n=allowGlobalConfirmation
choco feature enable -n=virusCheck
choco feature enable -n=allowEmptyChecksums

choco install pscx
choco install vcpython27
choco install git
choco install python2 --force

$env:Path += ";C:\python27\Scripts;C:\python27;C:\Program Files\Git\bin;C:\Program Files (x86)\Git\bin"
pip install virtualenv

Set-ItemProperty HKCU:\Software\PloneInstaller install_status "dependencies_installed"

git clone https://github.com/plone/simple-plone-buildout
Set-Location simple-plone-buildout
Copy-Item profiles\buildout.cfg.tmpl buildout.cfg
virtualenv -p C:\python27\python.exe env
env\Scripts\pip install -r requirements.txt
Set-ItemProperty HKCU:\Software\PloneInstaller install_status "starting_buildout"
env\Scripts\buildout
