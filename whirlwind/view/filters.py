from datetime import datetime
import pytz, sys, re
from dateutil import parser
try:
    import simplejson
except ImportError:
    import json as simplejson

class Filters():
    
    @staticmethod
    def strip_html(data):
        if not data :
            return
        p = re.compile(r'<[^<]*?/?>')
        return p.sub('', data)
    
    @staticmethod
    def long_timestamp(dt_str,tz="America/New_York"):
        utc_dt = NCFilters._convert_utc_to_local(dt_str,tz)
        if utc_dt:
            return utc_dt.strftime("%A, %d. %B %Y %I:%M%p")
        else:
            return dt_str
    
    @staticmethod
    def short_timestamp(dt_str,tz="America/New_York"):
        tz_dt = NCFilters._convert_utc_to_local(dt_str,tz)
        return tz_dt.strftime("%m/%d/%Y %I:%M")
    
    @staticmethod
    def short_date(dt_str,tz="America/New_York"):
        tz_dt = NCFilters._convert_utc_to_local(dt_str,tz)
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
        url = re.sub(r'[^0-9a-zA-Z]', '_',str)
        url = re.sub('_+', '_',url)
        #max 32 chars.
        if len(url) > 32 :
            url = url[0:32] 
        return url
    
    @staticmethod
    def pluralize(str):
        pl = Pluralizer()
        return pl.plural(str)
        


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
        