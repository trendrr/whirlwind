from tornado.web import RequestHandler, HTTPError
from mako.template import Template
from mako.lookup import TemplateLookup
from tornado.options import options
import re, sys, threading
from tornado import web
from urllib import unquote
from whirlwind.middleware import MiddlewareManager

from tornado import ioloop

class BaseRequest(RequestHandler):
    
    __template_exists_cache = {}
    
    def __init__(self, application, request):
        RequestHandler.__init__(self, application, request)
        self._current_user = None
        self.middleware_manager = MiddlewareManager(self)
        self._is_threaded = False
        self._is_whirlwind_finished = False
    
    def template_exists(self, template_name):
        tmp = self.__template_exists_cache.get(template_name, None)
        if tmp != None:
            print "found in cache: " + template_name
            return tmp
        
        lookup = self._get_template_lookup()
        try:
            new_template = lookup.get_template(template_name)
            if new_template :
                self.__template_exists_cache[template_name] = True
                return True
        except Exception as detail:
            print 'run-time error in BaseRequest::template_exists - ', detail
        self.__template_exists_cache[template_name] = False   
        return False
        
        
    def _get_template_lookup(self) :
        from whirlwind.view.filters import Cycler
        Cycler.cycle_registry = {}
        
        return TemplateLookup(
            directories=[options.template_dir], 
            module_directory=options.mako_modules_dir, 
            output_encoding='utf-8', 
            encoding_errors='replace',
            imports=[
                'from whirlwind.view.filters import Filters, Cycler',
            ]
        )
        
    def render_template(self,template_name, **kwargs):
        lookup = self._get_template_lookup()
        new_template = lookup.get_template(template_name)
           
        #add all the standard variables.
        kwargs['current_user'] = self.get_current_user()
        kwargs['render_as'] = self.get_argument('render_as', 'html')
        
        kwargs['is_logged_in'] = False
        if kwargs['current_user'] != None:
             kwargs['is_logged_in'] = True
        
        # allows us access to the request from within the template..
        kwargs['request'] = self.request
        
        self.middleware_manager.run_view_hooks(view=kwargs)
        
        self.finish(new_template.render(**kwargs))

    '''
    hook into the end of the request
    '''
    def finish(self, chunk=None):      
        self._is_whirlwind_finished = True
        #run all middleware response hooks
        self.middleware_manager.run_response_hooks()
        if self._is_threaded :
            
            print "Thread finished.  setting ioloop callback..", str(threading.currentThread())
            self._chunk = chunk
            ioloop.IOLoop.instance().add_callback(self.threaded_finish_callback)
            return
            
        super(BaseRequest, self).finish(chunk)
        
    
    '''
     this is called by the ioloop when the thread finally returns.
    '''
    def threaded_finish_callback(self):
        print "In the finish callback thread is ", str(threading.currentThread()) 
        super(BaseRequest, self).finish(self._chunk)
        self._chunk = None;
        
    
    
    '''
    hook into the begining of the request here
    '''
    def prepare(self):
        #run all middleware request hooks
        self.middleware_manager.run_request_hooks()
            
    def get_current_user(self):
        return self._current_user
        
    def set_current_user(self, user):
        self._current_user = user        
    
    def is_logged_in(self):
        return self.get_current_user() != None
    
    '''
    gets all the request params as a map. cleans them all up ala get_argument(s)
    '''
    def get_arguments_as_dict(self):
        params = {}
        retVals = []
        for key in self.request.arguments:
            values = self.get_arguments(key)
            k = unquote(key)
            if len(values) == 1 :
                params[k] = values[0]
            else :
                params[k] = values
            
        return params
    
    '''
    Same as get_argument but will return a list 
    if no arguments are supplied then a dict of all
    the arguments is returned.
    '''
    def get_arguments(self, name=None,  default=None, strip=True):
        if name is None :
            return self.get_arguments_as_dict()
        
        values = self.request.arguments.get(name, None)
        if values is None:
            return default
        
        retVals = []
        for val in values :
            value = self._cleanup_param(val, strip)
            retVals.append(value)
        return retVals
    
    def get_argument(self, name, default=RequestHandler._ARG_DEFAULT, strip=True):
        value = super(BaseRequest, self).get_argument(name, default, strip)
        if value == default :
            return value
        return unquote(value)
    
    '''
        cleans up any argument
        removes control chars, unescapes, ect
    '''
    def _cleanup_param(self, val, strip=True):
        # Get rid of any weird control chars
        value = re.sub(r"[\x00-\x08\x0e-\x1f]", " ", val)
        value = web._unicode(value)
        if strip: value = value.strip()
        return unquote(value)   
    
    def get_username(self):
        if self.get_current_user() :
            return self.get_current_user()['_id']
        return None
        
    
    def write(self,chunk,status=None):
        if status:
            self.set_status(status)
        
        RequestHandler.write(self, chunk)
    
    def get_error_html(self, status_code, **kwargs): 
        print 'GOT ERROR: ', status_code
        
        if kwargs.has_key('exception'):
            print kwargs['exception']
        
        if status_code == 404 :
            self.redirect('/404')
        else : # call super.
            self.redirect('/error')
