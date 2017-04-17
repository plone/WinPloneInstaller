#
# InstallPloneWSL.ps1
#
if ((Get-WmiObject win32_operatingsystem).buildNumber -ge '15063') 
{
    if ((Invoke-Elevated Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq "Enabled")
    {
        bash -c "../bash/plone.sh"
    }
    else {exit 2}
}
else {exit 1} 

#exit 1 - not a high enough build number to run this script
#exit 1 - WSL is not enabled on this machine  