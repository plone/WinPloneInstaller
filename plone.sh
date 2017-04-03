#!/bin/bash
sudo su
apt-get install python-setuptools python-dev build-essential libssl-dev libxml2-dev libxslt1-dev libbz2-dev libjpeg62-dev
apt-get install libreadline-dev wv poppler-utils
wget --no-check-certificate "https://launchpad.net/plone/5.0/5.0.4/+download/Plone-5.0.4-UnifiedInstaller.tgz" # Remember it's possible for wget to not be available
tar -xf Plone-5.0.4-UnifiedInstaller.tgz #wtf
cd Plone-5.0.4-UnifiedInstaller
./install.sh