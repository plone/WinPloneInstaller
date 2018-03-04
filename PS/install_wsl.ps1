$ploneKey = 'HKCU:\Software\PloneInstaller'
if ((Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq "Enabled") {
  Write-Host "Your browser will open to Microsoft's free Ubuntu App page.";
  Write-Host "Please 'Get the app' and 'Launch' it to complete its installation.";
  Write-Host "You will then configure a username and password for the app, and exit the app.";
  Write-Host "Once this is completed and you exited the app, press any key to continue installing Plone.";
  $browser = (New-Object -Com Shell.Application).Open("https://www.microsoft.com/store/productId/9NBLGGH4MSV6");
  while (!((bash -c "echo test") -eq "test")) {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User") #refresh system path so bash will be included
    Write-Host -NoNewLine "Press any key once Ubuntu has finished installing...";
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown");
  }
  Set-ItemProperty -Path $ploneKey install_status "wsl_installed";
} else {
  Write-Host -NoNewLine "WSL Not Enabled, have you restarted yet?";
  $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown");
  exit 1 # WSL is not enabled on this machine
}
