echo "**Please enter your Linux Subsystem password to allow WinPloneInstaller to continue."
sudo echo "**Updating/Upgrading WSL"
sudo apt-get -y update
sudo apt-get -y upgrade
echo "**Installing dependencies on WSL"
sudo apt-get -y install python-setuptools python-dev build-essential libssl-dev libxml2-dev libxslt1-dev libbz2-dev libjpeg62-dev
sudo apt-get -y install libreadline-dev wv poppler-utils
#echo "**Downloading the Plone Universal Installer"
#wget --no-check-certificate "https://launchpad.net/plone/5.0/5.0.7/+download/Plone-5.0.7-UnifiedInstaller.tgz" #this wget call will get moved to a separate unpiped PS process
echo "**Extracting the Plone Universal Installer"
tar -xf ./Plone-5.0.7-UnifiedInstaller.tgz
cd Plone-5.0.7-UnifiedInstaller
echo "**Launching the Plone Universal Installer. This may take a while..."