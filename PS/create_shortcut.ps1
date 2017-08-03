$ploneKey = 'HKCU:\Software\PloneInstaller'
$path = (Get-ItemProperty -Path $ploneKey -Name base_path).base_path
Set-Location $path
$shell = New-Object -comObject WScript.Shell
$shortcut = $shell.CreateShortcut("$Home\Desktop\Plone.lnk")
$target = "C:\Windows\System32\bash.exe"
$arguments = "-c '/etc/Plone/zinstance/bin/plonectl console'"
$shortcut.TargetPath = $target
$shortcut.Arguments = $arguments
$iconPath = "C:\Program` Files\plone.ico"
Copy-Item .\resources\plone.ico $iconPath
$shortcut.IconLocation = $iconPath
$Shortcut.Save()