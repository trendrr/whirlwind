#from tornado import web
import hashlib
import os, StringIO, pycurl
from tornado.web import *


import sys
import threading
import time
import weakref
from Queue import Queue


from tornado import ioloop
from tornado import stack_context

def threaded(method):
    '''
        Makes a regular controller action threaded.
    '''
    @asynchronous
    def wrapper(self, *args, **kwargs):
        self._is_threaded = True        
        action = ThreadedAction(method, self, *args, **kwargs)
        ThreadPool.instance().add_task(action.do_work)

    return wrapper


class ThreadedAction():
    
    def __init__(self, method, controller, *args, **kwargs):
        self._method = method
        self._controller = controller
        self._args = args
        self._kwargs = kwargs
        
    
    def do_work(self):
        try :
            # TODO: handle controllers that return a value. 
            # (think tornado considers that a json response)
            self._method(self._controller, *self._args, **self._kwargs)
            if not self._controller._is_whirlwind_finished :
                self._controller.finish()
        except Exception,e :
            self._controller._handle_request_exception(e)
        
        

'''
    Simple Threadpool implementation.  
    
    
'''
class ThreadPool():
    
    '''
        Pool of threads consuming tasks from a queue
        
        Note: I'm not crazy about the fixed threadpool implementation. 
        TODO: should have a max_threads argument, then we can build up to that as needed and 
        reap unused threads. 
        -dustin
    '''
    def __init__(self, num_threads=10):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): ThreadPoolWorker(self.tasks)

    '''
        Submits a task to the threadpool
        callback will be called once the task completes.
    '''
    def add_task(self, func, callback=None):
        """Add a task to the queue"""
        self.tasks.put((func, callback))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()    
    
    '''
        Returns the global threadpool.  Use this in almost all cases.
    '''
    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance


class ThreadPoolWorker(threading.Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        threading.Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            func, callback = self.tasks.get()
            try: func()
            except Exception, e: print e
            if callback :
                callback()
            self.tasks.task_done()        