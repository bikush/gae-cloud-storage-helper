import webapp2
import jinja2
import os
from storage_example.upload_handler import UploadHandler, URL_UPLOAD
from cloud_helper.cloud_handler import CloudStorageHandler
from google.appengine.api import app_identity
from cloud_helper.cloud_helper import CloudStorageHelper


def setup_jinja(folder_name):
    template_dir = os.path.join(os.path.dirname(__file__), folder_name)
    return jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


class MainHandler(webapp2.RequestHandler):
    def get(self, *args):
        self.response.write( "LOCAL" if self.app.config.get('is_local', False) else "GLOBAL" )
   
   
config = {
    'jinja_env' : setup_jinja('templates'),
    'is_local' : app_identity.get_default_version_hostname().startswith('localhost:')
}

app = webapp2.WSGIApplication([
    (URL_UPLOAD + r'/(.*)', UploadHandler),
    (CloudStorageHelper.default_local_url + r'/(.*)', CloudStorageHandler),
    (".*", MainHandler)
], config=config, debug=True)

