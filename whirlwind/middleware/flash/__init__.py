from collections import defaultdict

class Flash(defaultdict):
    def __init__(self, *args, **kwargs):
        #self.session = kwargs.pop('session',False)
        super(Flash, self).__init__(list, *args, **kwargs)
        
    '''
    make commonly used flashes available as attributes
    '''
    error = property(lambda s: s.get('error', []), lambda s, v: s.__setitem__('error',v))
    notice = property(lambda s: s.get('notice', []), lambda s, v: s.__setitem__('notice',v))
    success = property(lambda s: s.get('success', []), lambda s, v: s.__setitem__('success',v))
    info = property(lambda s: s.get('info', []), lambda s, v: s.__setitem__('info',v))
    
    '''
    if used as a string, return the first message found
    '''
    def __str__(self):        
        if len(self) > 0:
            if len(self.values()[0]) > 0:
                return self.values()[0][0]
        return ""
    
    '''
    get a value from our session
    '''
    def __getitem__(self, key):
        return self.get(key, [])
        
    '''
    set a value
    '''
    def __setitem__(self, key, value):
        if key in self:
            vals = self[key]
            vals.append(value)
            self.update({key:vals})
        else:
            self.update({key : [value]})
    
    '''    
    evaluate to True if there is at least one non-empty message
    '''
    def __nonzero__(self):
        return len(str(self)) > 0    
