# Setup instructions

## On Ubuntu (recommended)

### install python dev
`sudo apt-get install python-dev`

### install tornado, follow instructions on:
http://www.tornadoweb.org/documentation#download

### install the python setup tools
`sudo apt-get install python-setuptools`

### upgrade setuptools
`sudo easy_install -U setuptools`

### install required python modules
<pre>
sudo easy_install Mako
sudo easy_install MongoKit
sudo easy_install python-dateutil
sudo easy_install pytz
</pre>

### install whirlwind
`download a copy of whirlwind from https://github.com/trendrr/whirlwind/ or alternately clone a copy of the git repo`
 
### untar/unzip archive
`tar -xzf trendrr-whirlwind-5c17ff8.tar.gz`

### change to whirlwind directory
`cd whirlwind`

### run the setup script
`sudo python setup.py install`

### to create a whirlwind app
`whirlwind-admin.py --create-application myapp`

### fill in env specific settings in settings file [config/settings.py]
<pre>
generate a cookie secret (copy output to config/settings.py)
whirlwind-admin.py --gcs
</pre>

### to start app
`python main.py`
