echo "**Installing Chocolatey package manager"
Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy unrestricted -Force
iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))
echo "*!Chocolatey Installed"