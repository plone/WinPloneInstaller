$ploneKey = 'HKCU:\Software\PloneInstaller'

if ((Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq "Enabled") {
    Invoke-Elevated lxrun /install /y
    Set-ItemProperty -Path $ploneKey install_status "wsl_installed"
} else {
    Write-Host -NoNewLine "WSL Not Enabled, have you restarted yet?"
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
} #exit 1 - WSL is not enabled on this machine  