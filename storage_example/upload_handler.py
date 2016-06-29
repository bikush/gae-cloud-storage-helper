# Created by Bruno Mikus (github.com/bikush)
# License: Apache 2.0

import webapp2
from cloud_helper.cloud_helper import CloudStorageHelper
from cloud_helper.cloud_handler import CloudStorageHandler

URL_UPLOAD = '/upload'
URL_UPLOAD_HTML = "upload.html"
        
class UploadHandler(webapp2.RequestHandler):  
    """
    Displays an upload page that enables upload of an image to a given path.
    Handles post from the image upload form.
    """
    
    def render(self, template, **kw):
        """
        Jinja2 render helper function.
        """ 
        render_out = ""
        jinja_env = self.app.config.get("jinja_env")
        if jinja_env:
            t = jinja_env.get_template(template)
            render_out = t.render(kw)
        self.response.out.write(render_out)
        
        
    def get(self, *args):   
        """
        Generates the upload html page for file determined by the url.
        e.g. localhost:8080/upload/some/path will generate upload page for an
        image named some/path. This image will be available on 
        localhost:8080/storage/some/path or on
        https://storage.googleapis.com/BUCKET_NAME/some/path when online.
        """    
        
        path = CloudStorageHelper.read_path_from_handler_args(*args) 
        if len(path) == 0:
            self.render(URL_UPLOAD_HTML)
        else:
            file_data = CloudStorageHelper.read_file(path)
            storage_url = CloudStorageHelper.get_storage_url_base(self.app.config)
                
            jinja_settings = { "url_update" : (URL_UPLOAD + "/" + path) }
            if len(file_data) > 0:
                jinja_settings["file_url"] = CloudStorageHelper.create_complete_url(path, local_url=storage_url)
        
            self.render(URL_UPLOAD_HTML, **jinja_settings)
    
    
    def post(self, *args):   
        """
        Places the given file in the cloud storage when online, or development
        blobstore when local. Accepts files whose name ends with png/jpg/jpeg
        and are less than 1MB.
        """  
        
        path = CloudStorageHelper.read_path_from_handler_args(*args) 
        if len(path) == 0:
            self.redirect(URL_UPLOAD)
            return
             
        the_file = self.request.POST.multi['file'].file
        the_file_name = self.request.POST.multi['file'].filename
        data = the_file.read()
        file_ext = the_file_name.split('.')[-1].lower()
        
        content_type = None
        if file_ext == "png":
            content_type = "image/png"
        elif file_ext == "jpg" or file_ext == "jpeg":
            content_type = "image/jpeg"
            
        content_size = len(data)
        
        # file size 1MB
        if content_type != None and content_size < 1024*1024 and content_size > 0:                
            print "received data ", the_file_name, ", length ", str(len(data)), ", starts ", data[:100]
            CloudStorageHelper.create_file(path, content_type, data)
        
        self.render(URL_UPLOAD_HTML)
    
