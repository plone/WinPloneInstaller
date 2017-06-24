echo "**Configuring Chocolatey"
choco feature enable -n=allowGlobalConfirmation
choco feature enable -n=virusCheck
choco feature enable -n=allowEmptyChecksums

echo "**Installing pscx"
choco install pscx -y
echo "**Installing MS VC++ Compiler for Python 2.7"
choco install vcpython27 -y
echo "**Installing git"
choco install git -y
echo "**Installing Python 2.7"
choco install python2 --force

$env:Path += ";C:\python27\Scripts;C:\python27;C:\Program Files\Git\bin;C:\Program Files (x86)\Git\bin"
echo "**Installing virtualenv"
pip install virtualenv

echo "**All dependencies installed. Cloning simple-plone-buildout"
git clone https://github.com/plone/simple-plone-buildout
Set-Location simple-plone-buildout
Copy-Item profiles\buildout.cfg.tmpl buildout.cfg
virtualenv -p C:\python27\python.exe env
env\Scripts\pip install -r requirements.txt
echo "**Starting buildout, this may take a while..."
env\Scripts\buildout