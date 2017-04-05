#
# InstallPloneWSL.ps1
#
if ((Get-WmiObject win32_operatingsystem).buildNumber -ge '14393') 
{
if ((Invoke-Elevated Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq "Enabled")
{
#bash -c "sudo yes | apt-get install python-setuptools python-dev build-essential libssl-dev libxml2-dev libxslt1-dev libbz2-dev libjpeg62-dev"
}
else {exit 2}
}
else {exit 1} 

#exit 1 - not a high enough build number to run this script
#exit 1 - WSL is not enabled on this machine  