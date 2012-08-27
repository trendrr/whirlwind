from datetime import datetime
import pytz, sys, re, locale
from dateutil import parser
from tornado.options import options

try:
    import simplejson
except ImportError:
    import json as simplejson

class Filters():
    
    '''
        Checks whether the passed in value is considered useful otherwise will return None

        will return None on the following values:
            None
            ''
            'null'
            'undefined'
            {}
    '''
    @staticmethod
    def val(val):
        if val == None :
            return None
        if val == 'null' :
            return None
        if val == 'undefined' :
            return None
        if val == 0 :
            return val
        if isinstance(val, basestring) and len(val) == 0 :
            return None
        if isinstance(val, dict) and len(val) == 0 :
            return None
        return val
    
    @staticmethod
    def version():
    	try:
      		return options.version
      	except:
      		return ''
    
    @staticmethod
    def str(val):
        if not val:
            return ''
        #TODO: sensibly handle:
        # dicts => json 
        # dates => pretty 
        # numbers => add commas
        return str(val)
        
    
    '''
        Checks for various styles of true.
        matches on True, 'true', 'on'
    '''
    @staticmethod
    def is_true(val):        
        if not val :
            return False
        if isinstance(val, basestring) :
            if val == 'True' or val == 'true' or val == 'on' :
                return True
            return False
        if val == True :
             return True
        return False
    
    
    @staticmethod
    def strip_html(data):
        if not data :
            return
        p = re.compile(r'<[^<]*?/?>')
        return p.sub('', data)
    
    @staticmethod
    def long_timestamp(dt_str,tz="America/New_York"):
        utc_dt = Filters._convert_utc_to_local(dt_str,tz)
        if utc_dt:
            return utc_dt.strftime("%A, %d. %B %Y %I:%M%p")
        else:
            return dt_str
    
    @staticmethod
    def short_timestamp(dt_str,tz="America/New_York"):
        tz_dt = Filters._convert_utc_to_local(dt_str,tz)
        return tz_dt.strftime("%m/%d/%Y %I:%M")
    
    @staticmethod
    def short_date(dt_str,tz="America/New_York"):
        tz_dt = Filters._convert_utc_to_local(dt_str,tz)
        return tz_dt.strftime("%m/%d/%Y")
    
    @staticmethod
    def ellipsis(data,limit,append='...'): 
        return (data[:limit] + append) if len(data) > limit else data
    
    '''
     filter to translate a dict to json
    '''
    @staticmethod
    def to_json(dict):
        return simplejson.dumps(dict, True) 
        
    @staticmethod
    def idize(str):
        return (re.sub(r'[^0-9a-zA-Z]', '_',str)).lower()

    @staticmethod
    def _convert_utc_to_local(utc_dt,tz):
        try:
            print utc_dt
            local = pytz.timezone(tz)
            local_dt = utc_dt.replace(tzinfo = local)
            return local_dt.astimezone (pytz.utc)
        except Exception:
            print sys.exc_info()
            return None
    
    @staticmethod
    def url_pretty(str):
        if not str :
            return

        url = re.sub(r'[^0-9a-zA-Z]', '_',Filters.str(str))
        url = re.sub('_+', '_',url)
        #max 32 chars.
        if len(url) > 32 :
            url = url[0:32] 
        return url
    
    @staticmethod
    def add_commas(val,as_data_type='int',the_locale=locale.LC_ALL):
        locale.setlocale(the_locale, "")
        if as_data_type == 'int':
            return locale.format('%d', int(val), True)
        elif as_data_type == 'float':
            return locale.format('%f', float(val), True)
        else:
            return val
        
    @staticmethod
    def get_time_string(str):
        if str == "N/A":
            return str
        
        parts = str.split("/")
        isPM = parts[0].find('am') == -1
        if not isPM:
            parts[0] = parts[0].replace("am","")
        parts[1] = parts[1].replace("c","")
        if(len(parts[0]) >= 3):
            if(len(parts[0]) == 4):
                parts[0] = parts[0][0:2] + ":" + parts[0][2:]
            else:
                parts[0] = parts[0][:1] + ":" + parts[0][1:]
        if(len(parts[1]) >= 3):
            if(len(parts[1]) == 4):
                parts[1] = parts[1][0:2] + ":" + parts[1][2:]
            else:
                parts[1] = parts[1][:1] + ":" + parts[1][1:]
                
                
        if isPM:
            time = parts[0] + "/" + parts[1] + "c"
        else:
            time = parts[0] + "am/" + parts[1] + "c"
        
        return time
    
    
    
            
    @staticmethod
    def pluralize(str):
        pl = Pluralizer()
        return pl.plural(str)

    '''
        Does a get on the dict.  will work with dot operator, and not throw an exception
        returns default if the key doesn't work
        
        will also work to reach into lists via integer keys.
        
        example:
        {
            'key1' : {
                'subkey' : [{'subsubkey1':9},{}]
            }
        }
        
        Filters.dict_get('key1.subkey.0.subsubkey1') => 9
    '''
    @staticmethod
    def dict_get(dict, key, default=None):
        #Surround this with try in case key is None or not a string or something
        try:
            keys = key.split(".")
        except:
            return default
        
        tmp = dict
        for k in keys :
            try:
                tmp = tmp[k]
            except TypeError:
                #Issue may be that we have something like '0'. Try converting to a number
                try:
                    tmp = tmp[int(k)]
                except:
                    #Either couldn't convert or went out of bounds on list
                    return default
            except:
                #Exception other than TypeError probably missing key, so default
                return default
        return tmp


class Pluralizer():
    #
    # (pattern, search, replace) regex english plural rules tuple
    #
    rule_tuple = (
                  ('[ml]ouse$', '([ml])ouse$', '\\1ice'),
                  ('child$', 'child$', 'children'),
                  ('booth$', 'booth$', 'booths'),
                  ('foot$', 'foot$', 'feet'),
                  ('ooth$', 'ooth$', 'eeth'),
                  ('l[eo]af$', 'l([eo])af$', 'l\\1aves'),
                  ('sis$', 'sis$', 'ses'),
                  ('man$', 'man$', 'men'),
                  ('ife$', 'ife$', 'ives'),
                  ('eau$', 'eau$', 'eaux'),
                  ('lf$', 'lf$', 'lves'),
                  ('[sxz]$', '$', 'es'),
                  ('[^aeioudgkprt]h$', '$', 'es'),
                  ('(qu|[^aeiou])y$', 'y$', 'ies'),
                  ('$', '$', 's')
                  )

    def regex_rules(rules=rule_tuple):
        for line in rules:
            pattern, search, replace = line
            yield lambda word: re.search(pattern, word) and re.sub(search, replace, word)
 
    def plural(noun):
        for rule in regex_rules():
            result = rule(noun)
            if result:
                return result
    
    
    

class Cycler():
    cycle_registry = {}
    
    @staticmethod
    def uuid():
        import uuid
        return uuid.uuid1()
    
    @staticmethod
    def cycle(values,name='default'):
        if name in Cycler.cycle_registry:
            try:
                return Cycler.cycle_registry[name].next()
            except StopIteration:
                Cycler.cycle_registry[name] = iter(values)
                return Cycler.cycle_registry[name].next()
        else:
            Cycler.cycle_registry[name] = iter(values)
            return Cycler.cycle_registry[name].next()
        