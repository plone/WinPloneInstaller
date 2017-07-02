$requiredBuild = 15063
$buildNumber = [int](Get-WmiObject win32_operatingsystem).buildNumber
if ($buildNumber -lt $requiredBuild) {
    echo "**This system has Windows build number $buildNumber."
    echo "**Windows 10 with Creator's Update (build 15063) required to install on WSL (recommended)"
    echo "*!Installing Plone with buildout"
} else {
    echo "**Plone can be installed on WSL (recommended) on this system!"
    reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock" /t REG_DWORD /f /v "AllowDevelopmentWithoutDevLicense" /d "1"
    if ((Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq "Enabled") {
        if (Get-Command bash -ErrorAction SilentlyContinue) { # WSL is already installed...will not override current setup, WinPloneInstaller will call install_wsl.ps1
            echo "**WSL is installed on this machine"
            echo "*!Installing Plone on WSL"
        } else { #WinPloneInstaller.py will call install_wsl.ps1
            echo "**WSL is enabled on this machine"
            echo "*!Installing WSL"
        }
    } else { #WinPloneInstaller.py will complete this code block
        $installerPath = (Get-ItemProperty -Path HKCU:\Software\PloneInstaller -Name installer_path).installer_path
        Set-ItemProperty HKCU:\Software\PloneInstaller install_status "enabling_wsl"
        Set-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce plone_installer "$installerPath"
        
        Enable-WindowsOptionalFeature -Online -NoRestart -FeatureName Microsoft-Windows-Subsystem-Linux
        echo "**Enabling WSL."
        echo "*!Plone must restart the machine"
    }
}