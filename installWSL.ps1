#
# installWSL.ps1
#
If (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
	$arguments = "& '" + $myinvocation.mycommand.definition + "'"
	Start-Process powershell -Verb runAs -ArgumentList $arguments
	Break
}

if ((Get-WmiObject win32_operatingsystem).buildNumber -ge '15063') 
{
    if (Invoke-Elevated (Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq "Enabled")
    {
        Invoke-Elevated lxrun /install /y
        "Windows Subsystem for Linux Installed" | Add-Content 'installLog.txt'
        Set-Location HKCU:\Software\PLONE
        Set-ItemProperty . install_status "wsl_installed"
    }
    else {exit 2}
}
else {exit 1} 

#exit 1 - not a high enough build number to run this script
#exit 1 - WSL is not enabled on this machine  