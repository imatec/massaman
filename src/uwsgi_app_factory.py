this_app_dir = "/www/localhost_massaman/src/"
activate_this = "/www/localhost_massaman/src/venv/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))
import sys, os
# import logging
# logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, this_app_dir)
os.chdir(this_app_dir)
from app import create_app
application = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == "__main__":
    application.run()
