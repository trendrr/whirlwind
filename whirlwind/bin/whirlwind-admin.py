#!/usr/bin/env python

import whirlwind
import os
import re
import subprocess
import logging
import optparse
import distutils
from distutils import dir_util

'''
whirlwind.py --version

whirlwind.py --create-application app_name
'''

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

def main():
    
    usage = "usage: %prog [options [args]]"
    parser = optparse.OptionParser(usage)
    
    parser.add_option("--ca", "--create-application", 
                    dest="create_app",
                    metavar="FILE",
                    action="store_true",
                    default=False,
                    help="Creates an application structure")
    
    parser.add_option("--v", "--version", dest="version",
                    action="store_true",
                    default=False,
                    help="Print the version info for this release of WhirlWind")
    
    options, args = parser.parse_args()

    if not options.create_app and not options.version:
        parser.error('Must choose one -- try --ca or --v')

    if options.create_app:
        
        if len(args) != 1:
            logging.error("Error no app name given")
            return
        
        #generate the template dir path        
        template_dir = os.path.join(whirlwind.__path__[0], 'conf', 'app_template')
        
        #copy the template files
        copied_files = dir_util.copy_tree(template_dir,args[0])
        
        #check that we copied files
        if len(copied_files) > 0:
            logging.info('Created %s' % options.create_app)
        else:
            logging.info('Error copying app template')
            
    if options.version:
        logging.info(whirlwind.get_version())

if __name__ == "__main__":
    main()