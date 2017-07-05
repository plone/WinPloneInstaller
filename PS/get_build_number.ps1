$buildNumber = [int](Get-WmiObject win32_operatingsystem).buildNumber
$ploneKey = 'HKCU:\Software\PloneInstaller'
Set-ItemProperty -Path $ploneKey build_number "$buildNumber"