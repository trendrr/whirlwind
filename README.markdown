# Welcome to whirlwind

Whirlwind is an easy-to-use meta framework that makes efficient use
of some of the fastest server-side and client-side technologies in an organized fashion. The goal of whirlwind is to speed up the configuration and development of scalable and efficient web applications. It's the glue for the seamless deployment of a combination of some useful parts of [well-known and robust technologies](https://github.com/trendrr/whirlwind/wiki/Credits). 

The code base of whirlwind was originally developed as the underlying web framework for the
social media metrics and analytics platform [**Trendrr**](http://trendrr.com).

Check out [our wiki for docs and more info](http://github.com/trendrr/whirlwind/wiki). 


## Setup instructions

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

**Note**: Before you create a whirlwind app, you should make sure you are in the
directory where you want your whirlwind app to be created. Therefore, make
sure to `cd` out of the whirlwind repository (in which you installed whirlwind) on your local machine. You should preferably create a new whirwind app in your home directory.

### to create a whirlwind app
<pre>
whirlwind-admin.py --create-application myapp
</pre>

### fill in env specific settings in settings file [config/settings.py]

Then `cd` into `myapp` (the name of the app you created)
<pre>
# generate a cookie secret
whirlwind-admin.py --gcs
</pre>

An auto-generated secret should be printed to standard output. 

### Set the variable `cookie_secret` in config/settings.py to the printed out secret 
<pre>
cookie_secret = "setthistoyourowncookiesecret"
</pre>

### to start app
<pre>
python main.py
</pre>

### that's it! now just point your browser to the app start page to see whirlwind in action. 
<pre>
http://localhost:8000/
</pre>

If you encounter any problems before, during, or after installation, please refer to our [FAQ](http://github.com/trendrr/whirlwind/wiki/FAQ).

Copyright &copy; 2010 Trendrr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.