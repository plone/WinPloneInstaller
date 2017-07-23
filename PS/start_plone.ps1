$ploneKey = 'HKCU:\Software\PloneInstaller'
$path = (Get-ItemProperty -Path $ploneKey -Name base_path).base_path
Set-Location $path