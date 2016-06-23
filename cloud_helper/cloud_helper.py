# Created by Bruno Mikus (github.com/bikush)
# License: Apache 2.0
"""
Collection of helpful functions to work with Cloud Storage.
"""

import traceback
import os
import cloudstorage as gcs
from google.appengine.api import app_identity


class CloudStorageHelper():
    """
    Exposes static methods and members that work with GAE Cloud Storage.
    Static members:
    - bucket_name: the bucket name given in an app.yaml, or default gcs bucket 
        name
    - is_local: naively determined by the hostname in app_identity, True when 
        localhost
    - default_local_url: start of a local url path where local 
        CloudStorageHandler serves
    """
    
    bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
    is_local = app_identity.get_default_version_hostname().startswith('localhost:')
    default_local_url = '/storage'
              
    @classmethod 
    def create_file(cls, filename, content_type, content):
        """
        Creates a file on the GCS with a given filename. Automatically prepends
        the bucket name to the filename.
        - filename: path and filename that will be used to store the content in
            the bucket. e.g. images/butterfly -> BUCKET_NAME/images/butterfly
        - content_type: MIME type of the file
        - content: file data
        """
        
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
        """
        Reads the contents of the file from GCS. For now, there is no feedback
        knowledge about content-type of the file. Returns empty string if file
        not found.
        - filename: path and file name of the requested resource. e.g. for a
            resource in a bucket /BUCKET_NAME/some/file the filename should be 
            given as some/file whiel BUCKET_NAME should be setup in the app.yaml
            file
        """
        
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
        """
        Creates a complete URL that can be used as a src or href in html. When
        serving online, the supplied url points to the google cloud storage
        api, and assumes that the file/bucket is shared publically.
        """
        
        if cls.is_local:
            return local_url + "/" + filename
        else:
            return "https://storage.googleapis.com" + cls.create_url(filename)
    
    
    @classmethod
    def read_path_from_handler_args(cls, *args):
        """
        Helper method for webapp handlers. Trims leading / from arguments
        and returns the path or empty string if no arguments provided.
        """
        path = args[0] if args != None and len(args) > 0 else ""
        if path.startswith('/'):
            path = path[1:]
        return path  
        
