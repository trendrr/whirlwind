#from tornado import web
from mako.template import Template
from lib.request import BaseRequest

from lib.mongo import Mongo
import hashlib
import os, StringIO, pycurl
from tornado.web import authenticated


class IndexHandler(BaseRequest):
    def get(self):
        template_values = {
            'page_id' : 'homepage'
        }
        self.render_template('/site/welcome.html',**template_values)       