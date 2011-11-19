import re

class Util(object):
    
    @staticmethod
    def normalize(username):
        if not username :
            return None
        #allow legal email address
        name = username.strip().lower()
        name = re.sub(r'[^a-z0-9\\.\\@_\\-~#]+', '', name)
        name = re.sub('\\s+', '_',name)
        
        #don't allow $ and . because they screw up the db.
        name = name.replace(".", "")
        name = name.replace("$", "")
        return name