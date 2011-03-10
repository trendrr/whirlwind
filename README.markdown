# Setup instructions

## On Ubuntu (recommended)

### install python dev
`sudo apt-get install python-dev`

### install the python setup tools
`sudo apt-get install python-setuptools`

### upgrade setuptools
`sudo easy_install -U setuptools`

### install required python modules
<pre>
sudo easy_install tornado
sudo easy_install Mako
sudo easy_install MongoKit
sudo easy_install python-dateutil
sudo easy_install pytz
</pre>

### clone whirlwind
`git clone git://github.com/trendrr/whirlwind.git`

### change to whirlwind directory
`cd whirlwind`

### run the setup script
`sudo python setup.py install`


## On Windows

### download and install python
http://www.python.org/download/

### download and install setup tools
http://pypi.python.org/pypi/setuptools#files

### upgrade setuptools
`easy_install -U setuptools`

### install required python modules
<pre>
easy_install tornado
easy_install Mako
easy_install MongoKit
easy_install python-dateutil
easy_install pytz
</pre>

### clone whirlwind
`git clone git://github.com/trendrr/whirlwind.git`

### change to whirlwind directory
`cd whirlwind`

### run the setup script
`python setup.py install`

------------------------------------------------------------------

## Now whirlwind is installed

### to create a whirlwind app
`whirlwind-admin.py --create-application myapp`

### fill in env specific settings in settings file [config/settings.py]
<pre>
generate a cookie secret (copy output to config/settings.py)
whirlwind-admin.py --gcs
</pre>

### to start app
`python main.py`
