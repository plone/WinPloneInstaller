echo "Updating/Upgrading WSL"
yes | apt-get update
yes | apt-get upgrade
echo "Installing dependencies on WSL"
apt-get -y install python-setuptools python-dev build-essential libssl-dev libxml2-dev libxslt1-dev libbz2-dev libjpeg62-dev
apt-get -y install libreadline-dev wv poppler-utils
echo "Downloading the Plone Universal Installer"
wget --no-check-certificate "https://launchpad.net/plone/5.1/5.1.0/+download/Plone-5.1.0-UnifiedInstaller.tgz"
echo "Extracting the Plone Universal Installer"
tar -xf ./Plone-5.1.0-UnifiedInstaller.tgz
rm -f Plone-5.1.0-UnifiedInstaller.tgz
cd Plone-5.1.0-UnifiedInstaller
echo "Launching the Plone Universal Installer. This may take a while..."