# Welcome to whirlwind

Whirlwind is an easy-to-use **MVC** framework written in **Python** that builds on top MongoDB and Tornado ([and others](https://github.com/trendrr/whirlwind/wiki/Credits)) to be super fast and scalable.

The code base of whirlwind was originally developed as the underlying web framework for the
social media metrics and analytics platform [**Trendrr**](http://trendrr.com).

Check out [our wiki for documentation](http://github.com/trendrr/whirlwind/wiki). 

Need help troubleshooting, refer to our [FAQ](https://github.com/trendrr/whirlwind/wiki/FAQ).


## Setup instructions

### On Linux/Unix/OSX

Requires [easy_install](http://pypi.python.org/pypi/setuptools) or better yet [pip](http://pypi.python.org/pypi/pip). 

### install required python modules
<pre>
sudo easy_install tornado
sudo easy_install Mako
sudo easy_install MongoKit
sudo easy_install python-dateutil
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

For instructions on how to install **whirlwind** on windows, visit [this page](https://github.com/trendrr/whirlwind/wiki/Windowsinstall).

### create a whirlwind app
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

### set the variable `cookie_secret` in config/settings.py to the printed out secret 
<pre>
cookie_secret = "setthistoyourowncookiesecret"
</pre>

### then start your app
<pre>
python main.py
</pre>

### that's it! now just point your browser to the app start page to see whirlwind in action. 
<pre>
http://localhost:8000/
</pre>

If you encounter any problems please refer to our [FAQ](http://github.com/trendrr/whirlwind/wiki/FAQ) for troubleshooting instructions or post a new issue.

Copyright &copy; 2010-2012 Trendrr

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