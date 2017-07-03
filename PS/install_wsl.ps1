if (Invoke-Elevated (Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq "Enabled") {
    Invoke-Elevated lxrun /install /y
    echo "**WSL Installed"
    echo "*!Installing Plone on WSL"
} else {
    echo "*!WSL Not Enabled, have you restarted yet?"
    exit 1
} #exit 1 - WSL is not enabled on this machine  