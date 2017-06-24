#Thank you Ben Armstrong for sharing this reliable script elevation strategy
#https://blogs.msdn.microsoft.com/virtual_pc_guy/2010/09/23/a-self-elevating-powershell-script/

$myWindowsID=[System.Security.Principal.WindowsIdentity]::GetCurrent()
$myWindowsPrincipal=new-object System.Security.Principal.WindowsPrincipal($myWindowsID)
 
$adminRole=[System.Security.Principal.WindowsBuiltInRole]::Administrator
 
if ($myWindowsPrincipal.IsInRole($adminRole)) {
   Set-ItemProperty HKCU:\Software\PloneInstaller install_status "elevated"
} else {
    Set-ItemProperty HKCU:\Software\PloneInstaller install_status "elevating"
    
    $ploneKey = 'HKCU:\Software\PloneInstaller'
    $installerPath = (Get-ItemProperty -Path $ploneKey -Name installer_path).installer_path
    Set-Location $installerPath
    $newProcess = new-object System.Diagnostics.ProcessStartInfo $installerPath;
    
    # Specify the current script path and name as a parameter
    #$newProcess.Arguments = $myInvocation.MyCommand.Definition;
    
    # Indicate that the process should be elevated
    $newProcess.Verb = "runas";
    
    # Start the new process
    [System.Diagnostics.Process]::Start($newProcess);
}