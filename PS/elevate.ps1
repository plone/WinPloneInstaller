#Thank you Ben Armstrong for sharing this reliable script elevation strategy
#https://blogs.msdn.microsoft.com/virtual_pc_guy/2010/09/23/a-self-elevating-powershell-script/

$ploneKey = 'HKCU:\Software\PloneInstaller'

$installerPath = (Get-ItemProperty -Path $ploneKey -Name installer_path).installer_path
$newProcess = new-object System.Diagnostics.ProcessStartInfo $installerPath;

$newProcess.Verb = "runas"; # Indicate that the process should be elevated

[System.Diagnostics.Process]::Start($newProcess); # Start the new process
Clear-Host
Write-Host "Preparing the Plone installer, an interface will appear."
Start-Sleep -s 3