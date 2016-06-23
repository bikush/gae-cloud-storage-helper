
import webapp2
from cloud_helper import CloudStorageHelper

class CloudStorageHandler(webapp2.RequestHandler):
   
    def get(self, *args):        
        path = CloudStorageHelper.read_path_from_handler_args(*args)
        storage_url = CloudStorageHelper.default_local_url
        if self.app.config != None:
            storage_url = self.app.config.get('storage_url', storage_url)
                
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
            self.redirect( CloudStorageHelper.create_complete_url(path, local_url=storage_url) )
       
        
