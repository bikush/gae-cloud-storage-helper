import webapp2
from cloud_helper.cloud_helper import CloudStorageHelper

URL_UPLOAD = '/upload'
URL_UPLOAD_HTML = "upload.html"
        
class UploadHandler(webapp2.RequestHandler):  
    
    def render(self, template, **kw): 
        render_out = ""
        jinja_env = self.app.config.get("jinja_env")
        if jinja_env:
            t = jinja_env.get_template(template)
            render_out = t.render(kw)
        self.response.out.write(render_out)
        
        
    def get(self, *args):       
        path = CloudStorageHelper.read_path_from_handler_args(*args) 
        if len(path) == 0:
            self.render(URL_UPLOAD_HTML)
        else:
            file_data = CloudStorageHelper.read_file(path)
                
            jinja_settings = { "url_update" : (URL_UPLOAD + "/" + path) }
            if len(file_data) > 0:
                jinja_settings["file_url"] = CloudStorageHelper.create_complete_url(path)
        
            self.render(URL_UPLOAD_HTML, **jinja_settings)
    
    
    def post(self, *args):     
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
        
        # file size 512KB
        if content_type != None and content_size < 512*1024 and content_size > 0:                
            print "received data ", the_file_name, ", length ", str(len(data)), ", starts ", data[:100]
            CloudStorageHelper.create_file(path, content_type, data)
        
        self.render(URL_UPLOAD_HTML)
    
