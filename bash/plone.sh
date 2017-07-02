touch test.txt
echo "**Please enter your Linux Subsystem password to allow WinPloneInstaller to continue."
sudo echo "**Updating/Upgrading WSL"
sudo apt-get -y update
sudo apt-get -y upgrade
echo "**Installing dependencies on WSL"
sudo apt-get -y install python-setuptools python-dev build-essential libssl-dev libxml2-dev libxslt1-dev libbz2-dev libjpeg62-dev
sudo apt-get -y install libreadline-dev wv poppler-utils
echo "**Extracting the Plone Universal Installer"
tar -xf ./PloneUnified.tgz
cd PloneUnified
echo "**Launching the Plone Universal Installer. This may take a while..."