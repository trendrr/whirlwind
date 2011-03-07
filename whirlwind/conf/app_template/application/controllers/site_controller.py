from whirlwind.core.request import BaseRequest
from whirlwind.db.mongo import Mongo
from tornado.web import authenticated
from whirlwind.view.decorators import route

@route('/')
class IndexHandler(BaseRequest):
    def get(self):
        #template context variables go in here
        template_values = {}
        
        self.render_template('/site/index.html',**template_values)