# Welcome to whirlwind
The goal of whirlwind is to provide an easy to use python framework built on top of todays fastest tech. The whirlwind code base was originally developed as the underlying web framework for the social media metrics and analytics platform [[http://www.trendrr.com]]. 

## Take a look around
* [[How to install Whirlwind | Install]]
* [[Credits]]
* [[Features Overview | Whirlwind-Features]]
* [[Docs]]


# Setup instructions

## On Ubuntu (recommended)

### install python dev
<pre>
sudo apt-get install python-dev
</pre>

### install the python setup tools
<pre>
sudo apt-get install python-setuptools
</pre>

### upgrade setuptools
<pre>
sudo easy_install -U setuptools
</pre>

### install required python modules
<pre>
sudo easy_install tornado
sudo easy_install Mako
sudo easy_install MongoKit
sudo easy_install python-dateutil
sudo easy_install pytz
</pre>

### clone whirlwind
<pre>
git clone git://github.com/trendrr/whirlwind.git
</pre>

### change to whirlwind directory
<pre>
cd whirlwind
</pre>

### run the setup script
<pre>
sudo python setup.py install
</pre>


## On Windows

### download and install python
<pre>
http://www.python.org/download/
</pre>

### download and install setup tools
<pre>
http://pypi.python.org/pypi/setuptools#files
</pre>

### upgrade setuptools
<pre>
easy_install -U setuptools
</pre>

### install required python modules
<pre>
easy_install tornado
easy_install Mako
easy_install MongoKit
easy_install python-dateutil
easy_install pytz
</pre>

### clone whirlwind
<pre>
git clone git://github.com/trendrr/whirlwind.git
</pre>

### change to whirlwind directory
<pre>
cd whirlwind
</pre>

### run the setup script
<pre>
python setup.py install
</pre>

## Now whirlwind is installed

### to create a whirlwind app
<pre>
whirlwind-admin.py --create-application myapp
</pre>

### fill in env specific settings in settings file [config/settings.py]
<pre>
generate a cookie secret (copy output to config/settings.py)
whirlwind-admin.py --gcs
</pre>

### to start app
<pre>
python main.py
</pre>

### thats it! now just point your browser to the app start page to see whirlwind in action. 
<pre>
http://localhost:8000/
</pre>
