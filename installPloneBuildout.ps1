#
# installPloneBuildout.ps1
#
pip install virtualenv
git clone https://github.com/plone/simple-plone-buildout
cd simple-plone-buildout
copy profiles\buildout.cfg.tmpl buildout.cfg
virtualenv env
env\Scripts\pip install -r requirements.txt
env\Scripts\buildout
bin\instance start