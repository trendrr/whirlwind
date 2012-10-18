#!/usr/bin/env python

import whirlwind
import os
import logging
import optparse
from distutils import dir_util

'''
whirlwind-admin.py --version

whirlwind-admin.py --create-application app_name

whirlwind-admin.py --generate-cookie-secret

whirlwind-admin.py --generate-model-indexes
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

    parser.add_option("--gcs", "--generate-cookie-secret", dest="generate_cookie_secret",
                    action="store_true",
                    default=False,
                    help="Generate a cookie secret hash")

    parser.add_option("--gmi", "--generate-model-indexes", dest="generate_model_indexes",
                action="store_true",
                default=False,
                help="Generate mongo indexes for your models")

    options, args = parser.parse_args()

    if not options.create_app and not options.version and not options.generate_cookie_secret and not options.generate_model_indexes:
        parser.error('Must choose one -- try --ca or --v or --gcs or --gmi')

    if options.create_app:

        if len(args) != 1:
            logging.error("Error no app name given")
            return

        #generate the template dir path
        template_dir = os.path.join(whirlwind.__path__[0], 'conf', 'app_template')

        #copy the template files
        copied_files = dir_util.copy_tree(template_dir, args[0])

        #check that we copied files
        if len(copied_files) > 0:
            logging.info('Created %s' % options.create_app)
        else:
            logging.info('Error copying app template')

    if options.version:
        logging.info(whirlwind.get_version())

    if options.generate_cookie_secret:
        import base64
        import uuid
        print(base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes))

    if options.generate_model_indexes:

        import sys
        import pkgutil
        from whirlwind.db.mongo import Mongo

        #insert the current dir into the path
        sys.path.insert(0, os.getcwd())

        #grab a settings path from our args if exists or assume relative default
        settings_module = args[0] if len(args) == 1 else 'config.settings'

        conf = __import__(settings_module)

        #connect to our db using our options set in settings.py
        Mongo.create(host=conf.settings.db_host, port=conf.settings.db_port)

        #import our default models package
        __import__('application.models')

        pkg_mods = sys.modules['application.models']

        #setup a prefix string
        prefix = pkg_mods.__name__ + "."

        #import all the modules in the models dir so the registration decorators fire
        for importer, modname, ispkg in pkgutil.iter_modules(pkg_mods.__path__, prefix):
            __import__(modname)

        #loop over the registered documents
        for doc, obj in Mongo.db.connection._registered_documents.iteritems():
            try:

                print 'Attempting to create index for ', doc
                #generate the index for this doc on the collection
                obj.generate_index(Mongo.db.connection[conf.settings.db_name][obj._obj_class.__collection__])
            except Exception, e:
                #barf up an error on fail
                print 'Could not create index for %s - exception: %s' % (doc, e.message)


if __name__ == "__main__":
    main()
