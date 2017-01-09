import os
import sys

import bottle


# Append current dir to path, so mod_wsgi can properly load modules
sys.path.append(os.path.dirname(__file__))

if True:
    import resources
    import routes

    # Reference scripts, register fp methods and add *.tpl files to path
    resources.initialize()

    # Is there a better way to reference the routes module?
    routes.refd = True


if '--debug' in sys.argv[1:] or 'SERVER_DEBUG' in os.environ:
    # Debug mode will enable more verbose output in the console window.
    # It must be set at the beginning of the script.
    bottle.debug(True)

if __name__ == '__main__':
    bottle.run(host='localhost', port=8080, reloader=False)

# Run with mod_wsgi
os.chdir(os.path.dirname(__file__))
application = bottle.default_app()
