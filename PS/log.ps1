function log($message) {
    $ploneKey = 'HKCU:\Software\PloneInstaller'
    $logFile = (Get-ItemProperty -Path $ploneKey -Name log_path).log_path
    echo $message
    $message | Add-Content $logFile
}