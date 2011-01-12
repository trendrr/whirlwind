#from tornado import web
from mako.template import Template
from whirlwind.core.request import BaseRequest

from whirlwind.db.mongo import Mongo
import hashlib
import os, StringIO, pycurl
from tornado.web import authenticated
from whirlwind.view.decorators import route

@route('/')
class IndexHandler(BaseRequest):
    def get(self):
        template_values = {
            'page_id' : 'homepage'
        }
        self.render_template('/site/welcome.html',**template_values)       