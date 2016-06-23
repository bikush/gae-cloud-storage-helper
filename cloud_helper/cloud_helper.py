import traceback
import os
import cloudstorage as gcs
from google.appengine.api import app_identity


class CloudStorageHelper():
    bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
    is_local = app_identity.get_default_version_hostname().startswith('localhost:')
    default_local_url = '/storage'
              
    @classmethod 
    def create_file(cls, filename, content_type, content):
        full_name = cls.create_url( filename )
        print ('Creating file %s' % full_name)
        
        try:
            write_retry_params = gcs.RetryParams(backoff_factor=1.1)
            gcs_file = gcs.open(full_name,
                                'w',
                                content_type=content_type,
                                retry_params=write_retry_params)
            gcs_file.write(content)
            gcs_file.close()
        except:
            traceback.print_exc()
            print "Could not write file at %s" % full_name
        
    
    @classmethod  
    def read_file(cls, filename):
        print ('Reading file %s' % filename)         
        full_name = cls.create_url( filename )
        
        contents = ""
        try:
            gcs_file = gcs.open(full_name)
            contents = gcs_file.read()
            gcs_file.close()
        except:
            traceback.print_exc()
            print "Could not read file at %s" % full_name
        
        return contents
    
    
    @classmethod
    def create_url(cls, filename):
        return "/" + cls.bucket_name + "/" + filename
   
   
    @classmethod
    def create_complete_url(cls, filename, local_url=default_local_url):
        if cls.is_local:
            return local_url + "/" + filename
        else:
            return "https://storage.googleapis.com" + cls.create_url(filename)
    
    
    @classmethod
    def read_path_from_handler_args(cls, *args):
        path = args[0] if args != None and len(args) > 0 else ""
        if path.startswith('/'):
            path = path[1:]
        return path  
        
