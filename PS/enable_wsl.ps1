$ploneKey = 'HKCU:\Software\PloneInstaller'
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock" /t REG_DWORD /f /v "AllowDevelopmentWithoutDevLicense" /d "1"

if ((Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq "Enabled") {
    if (Get-Command bash -ErrorAction SilentlyContinue) { # WSL is already installed...will not override current setup, WinPloneInstaller will call install_wsl.ps1
        Write-Output "**WSL is installed on this machine"
        Write-Output "*!Installing Plone on WSL"
    } else { #WinPloneInstaller.py will call install_wsl.ps1
        Write-Output "**WSL is enabled on this machine"
        Write-Output "*!Installing WSL"
    }
} else { #WinPloneInstaller.py will complete this code block
    $installerPath = (Get-ItemProperty -Path $ploneKey -Name installer_path).installer_path
    Set-ItemProperty -Path $ploneKey install_status "enabling_wsl"
    Set-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce plone_installer "$installerPath"
    
    Write-Output "*!Enabling WSL"
}