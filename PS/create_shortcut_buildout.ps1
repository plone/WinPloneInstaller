$ploneKey = 'HKCU:\Software\PloneInstaller'
$plonePath = (Get-ItemProperty -Path $ploneKey -Name install_directory).install_directory
$shell = New-Object -comObject WScript.Shell
$shortcut = $shell.CreateShortcut("$Home\Desktop\Plone.lnk")
$target = $plonePath+"\Plone\bin\instance.exe"
$arguments = "fg"
$shortcut.TargetPath = $target
$shortcut.Arguments = $arguments
$iconPath = "C:\Program` Files\plone.ico"
Copy-Item .\resources\plone.ico $iconPath
$shortcut.IconLocation = $iconPath
$Shortcut.Save()