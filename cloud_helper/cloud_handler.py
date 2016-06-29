# Created by Bruno Mikus (github.com/bikush)
# License: Apache 2.0
"""
Simple handler used to help serve files on local development
"""

import webapp2
from cloud_helper import CloudStorageHelper

class CloudStorageHandler(webapp2.RequestHandler):
    
    def get(self, *args):
        """
        Serves files in the local blobstore when run localy (CloudStorageHelper
        static member is_local). The storage_url can be setup through app config
        the default value is /storage.
        If serving online, redirects to the complete google storage api url.
        """
                
        path = CloudStorageHelper.read_path_from_handler_args(*args)
                
        if CloudStorageHelper.is_local:
            content = CloudStorageHelper.read_file(path)
            if len(content) == 0:
                self.response.headers['Content-Type'] = 'text/plain'        
                self.response.write( "File not found." );
            else:
                # TODO: send proper content type
                self.response.headers['Content-Type'] = 'image/jpeg'        
                self.response.write( content );
        else:
            storage_url = CloudStorageHelper.get_storage_url_base(self.app.config)
            self.redirect( CloudStorageHelper.create_complete_url(path, local_url=storage_url) )
       
