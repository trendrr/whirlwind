from tornado.web import _unicode
from tornado.web import RequestHandler, HTTPError
from mako.template import Template
from mako.lookup import TemplateLookup
from tornado.options import options
from tornado import escape
import datetime
import re, sys, threading, os, httplib, tornado.web
from urllib import unquote
from whirlwind.middleware import MiddlewareManager
from whirlwind.core.log import Log
from tornado.web import ErrorHandler
from tornado import ioloop
from pymongo import *
from whirlwind.view.filters import Filters
from whirlwind.view.paginator import Paginator
from whirlwind.core import dotdict
from whirlwind.db.mongo import Mongo
import pymongo
from tornado.websocket import WebSocketHandler

class WebSocketBaseRequest(WebSocketHandler):
	
	def __init__(self, application, request):
		WebSocketHandler.__init__(self, application, request)
		self._current_user = None
		self.middleware_manager = MiddlewareManager(self)
		self.db = Mongo.db.ui #@UndefinedVariable
		#run all middleware request hooks
		self.middleware_manager.run_request_hooks()
			
	def get_current_user(self):
		return self._current_user
		
	def set_current_user(self, user):
		self._current_user = user
	
	def is_logged_in(self):
		return self.get_current_user() != None


class BaseRequest(RequestHandler):
	
	__template_exists_cache = {}
	
	def __init__(self, application, request):
		RequestHandler.__init__(self, application, request)
		self._current_user = None
		self.middleware_manager = MiddlewareManager(self)
		self._is_threaded = False
		self._is_whirlwind_finished = False
		self.view = dotdict()
		self.db = Mongo.db.ui #@UndefinedVariable
	
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
		
		
	def _get_template_lookup(self,extra_imports=None) :
		from whirlwind.view.filters import Cycler
		Cycler.cycle_registry = {}
		
		filter_imports=[
			'from whirlwind.view.filters import Filters, Cycler',
		]
		
		if extra_imports:
			filter_imports.extend(extra_imports)
		
		
		if isinstance(options.template_dir,(list,tuple)):
			directory_paths = options.template_dir
		else:
			directory_paths = [options.template_dir]
			
		return TemplateLookup(
			directories=directory_paths, 
			module_directory=options.mako_modules_dir, 
			output_encoding='utf-8', 
			encoding_errors='replace',
			imports=filter_imports
		)
	
	
	#to support backwards compat
	def render_to_string(self,template_name,**kwargs):
		self.render_to_string(template_name,**kwargs)
	
	#returns the rendered output of a template populated with kwargs
	def render_string(self,template_name,**kwargs):
		lookup = self._get_template_lookup()
		new_template = lookup.get_template(template_name)
		kwargs = self.add_context_vars(**kwargs)
		return new_template.render(**kwargs)
	
	def add_context_vars(self,**kwargs):
		tornado_args = {
			"_": self.locale.translate,
			"current_user": self.get_current_user(),
			"datetime": datetime,
			"escape": escape.xhtml_escape,
			"handler": self,
			"json_encode": escape.json_encode,
			"linkify": escape.linkify,
			"locale": self.locale,
			"request": self.request,
			"reverse_url": self.application.reverse_url,
			"squeeze": escape.squeeze,
			"static_url": self.static_url,
			"url_escape": escape.url_escape,
			"xhtml_escape": escape.xhtml_escape,
			"xsrf_form_html": self.xsrf_form_html
		}
		tornado_args.update(self.ui)

		whirlwind_args = {
			"is_logged_in": self.get_current_user() != None,
			"render_as": self.get_argument("render_as", "html"),
			"dict_get" : Filters.dict_get
		}

		kwargs.update(whirlwind_args)
		kwargs.update(tornado_args)
		kwargs.update(self.view)
		
		return kwargs
	
	def render_template(self,template_name, **kwargs):
		lookup = self._get_template_lookup()
		new_template = lookup.get_template(template_name)

		kwargs = self.add_context_vars(**kwargs)
		
		self.middleware_manager.run_view_hooks(view=kwargs)
		
		self.finish(new_template.render(**kwargs))
	
	def get_nested_argument(self,prefix):
		'''
		get nested form input params as an object: project[name]
		'''
		
		params = self.get_arguments_as_dict()
		param_obj = {}
		
		for key in params.keys():
			if key.startswith(prefix):
				if '[' in key and ']' in key:
					param_obj[key[key.find("[")+1:key.find("]")]] = params[key]
				
		return param_obj
		
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
		value = _unicode(value)
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
		error_handler = WhirlwindErrorHandler(self.application, self.request, status_code=status_code)
		return error_handler.get_error_html(status_code, **kwargs) 

class WhirlwindErrorHandler(ErrorHandler):
	def get_error_html(self, status_code, **kwargs):
		self.require_setting("static_path")
		if status_code in [404, 500, 503, 403]:
			filename = os.path.join(self.settings['static_path'], 'errors/%d.html' % status_code)
			if os.path.exists(filename):
				f = open(filename, 'r')
				data = f.read()
				f.close()
				return data
		return "<html><title>%(code)d: %(message)s</title>" \
				"<body class='bodyErrorPage'>%(code)d: %(message)s</body></html>" % {
			"code": status_code,
			"message": httplib.responses[status_code],
		}

tornado.web.ErrorHandler = WhirlwindErrorHandler


class RequestHelpers(object):
	'''
	helper function to get chunks of large collections
	
	more efficient approach when paging large collections as long as 
	your using the standard automaticly generated mongo document _id
	
	PLEASE NOTE 
		only supports sorting by _id column
		
	'''
	@staticmethod
	def ranged_list(handler, table_class,select={}):
		max_id = handler.get_argument('max_id',False)
		min_id = handler.get_argument('min_id',False)
		
		if not max_id and not min_id:
			return False
			
		count = handler.get_argument('count',10)
		count = count if count >= 1 else 10
		order_by = handler.get_argument('order_by',None)
		
		sort = None
		
		if order_by:
			order = handler.get_argument('order',None)
			order = pymongo.DESCENDING if order.lower() == 'desc' else pymongo.ASCENDING
			sort = {
				order:'_id'
			}
		
		original_select = select
		if max_id != False:
			select['_id'] = {'$gt' : max_id}
		elif handler.get_argument('min_id',False):
			select['_id'] = {'$lt' : min_id}

		if sort:
			results = table_class.find(select).limit(count).sort(sort)
		else:
			results = table_class.find(select).limit(count)
		
		total = table_class.find(original_select).count()

		return [results,total]

	'''
	helper function to page lists of objects
	
	not as effient as paging by ids but is fine as long as your not paging large collections
	you must use this method if your using non standard document _ids 
	'''
	@staticmethod
	def paged_list(handler,table_class,select=None):
	
		page = handler.get_argument('page',1)
		page = page if page >= 1 else 1
		
		count = handler.get_argument('count',10)
		count = count if count >= 1 else 10
		
		sort = None
		order_by = handler.get_argument('order_by',None)
		
		try:
			if order_by:
				order = handler.get_argument('order',None)
				order = pymongo.DESCENDING if order.lower() == 'desc' else pymongo.ASCENDING
				sort = {
					order:order_by
				}

			if select:
				if sort:
					results = table_class.find(select).skip((page-1)*count).limit(count).sort(sort)
				else:
					results = table_class.find(select).skip((page-1)*count).limit(count)
				
				total = table_class.find(select).count()
			else:
				if sort:
					results = table_class.find().skip((page-1)*count).limit(count).sort(sort)
				else:
					results = table_class.find().skip((page-1)*count).limit(count)
					
				total = table_class.find().count()
	
			return Paginator(results,page,count,total)
	
		except:	
			return Paginator([],page,count,0)
	
	#delete checked list items
	@staticmethod
	def delete_selected(handler,pymongo_collection,feild_name='ids',return_stats=False):
		ids = handler.get_argument(feild_name,[])
		
		if len(ids) == 0: return False
		
		if not return_stats:
			pymongo_collection.remove(
				{'_id':{'$in':ids}
			})
			return True
		else:
			stats = {
				'requested':len(ids),
				'success':0,
				'failed':0
			}
			
			for _id in ids:
				try:
					pymongo_collection.remove({'_id':_id},True)
					stats['success'] += 1
				except Exception, ex:
					stats['failed'] += 1
					Log.error(ex.message)
		
			return stats