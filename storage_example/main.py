# Created by Bruno Mikus (github.com/bikush)
# License: Apache 2.0
"""
Example use of cloud_helper module.
A simple upload application that shows how can the GAE Cloud Storage be used
to upload files from your web application.
CloudStorageHandler is a simple request handler that can serve while deployed
on GAE or locally for testing purposes.
"""

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
    """
    Catches unsupported URLs. Tells if this instance is running locally or online.
    """
    def get(self, *args):
        self.response.write( "LOCAL" if self.app.config.get('is_local', False) else "GLOBAL" )
   
   
# Storage url is by default /storage, but can be something else
# This is usefull when testing locally, to quickly access the uplaoded files
#storage_url = '/s'
storage_url = CloudStorageHelper.default_local_url


# Configuration object for the webapp
config = {
    'jinja_env' : setup_jinja('templates'),
    'is_local' : app_identity.get_default_version_hostname().startswith('localhost:'),
    'storage_url' : storage_url
}

# UploadHandler serves the upload form
# CloudStorageHandler is used to serve files while testing locally
app = webapp2.WSGIApplication([
    (URL_UPLOAD + r'/(.*)', UploadHandler),
    (storage_url + r'/(.*)', CloudStorageHandler),
    (".*", MainHandler)
], config=config, debug=True)

