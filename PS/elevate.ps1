#Thank you Ben Armstrong for sharing this reliable script elevation strategy
#https://blogs.msdn.microsoft.com/virtual_pc_guy/2010/09/23/a-self-elevating-powershell-script/

$myWindowsID=[System.Security.Principal.WindowsIdentity]::GetCurrent()
$myWindowsPrincipal=new-object System.Security.Principal.WindowsPrincipal($myWindowsID)
 
$adminRole=[System.Security.Principal.WindowsBuiltInRole]::Administrator

$ploneKey = 'HKCU:\Software\PloneInstaller'

if ($myWindowsPrincipal.IsInRole($adminRole)) {
    echo "*!Running as Admin"
    Set-ItemProperty -Path $ploneKey install_status "elevated"
} else {
    echo "*!Elevating Process"

    $installerPath = (Get-ItemProperty -Path $ploneKey -Name installer_path).installer_path
    $newProcess = new-object System.Diagnostics.ProcessStartInfo $installerPath;
    
    Set-ItemProperty -Path $ploneKey install_status "elevated"

    $newProcess.Verb = "runas"; # Indicate that the process should be elevated
    
    [System.Diagnostics.Process]::Start($newProcess); # Start the new process
}