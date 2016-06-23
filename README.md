# GCS Helper
A GAE (google app engine) Cloud Storage helper classes for python webapp2 applications.

## Example

This app is currently live.

Every subpath on https://cloud-storage-test-1350.appspot.com/upload/ can have a resource uploaded, e.g. [example path][1] holds an image that is served on [this static URL][2].

You could upload your own images on any subpath, e.g. [https://cloud-storage-test-1350.appspot.com/upload/this/is/another/subpath][3].

Every subpath is mapped to the static serving cloud storage on **storage.googleapis.com/BUCKET_NAME/**
where BUCKET_NAME is the name of the bucket you created on your google cloud. When run locally, there is a Cloud Storage Handler that
serves the locally stored files (gcs development server stores them in a local blobstore).

## When to use

When you want to use Cloud Storage to hold your files, to upload them from your web application to cloud storage and to serve them to your users through static links to Cloud Storage.

You need an installed App Engine SDK for Python ([quickstart guide][4]).

When going live you need to create a bucket on Cloud Storage. You will need to enable billing. When you have your bucket, 
to make it available publically you need to change the persmissions ([described here][5]), easiest way to enter those
commands is through google cloud shell.


## What to use

What you need is in the cloud_helper module. Common methods that can be found around the internet are in the CloudStorageHelper class.

CloudStorageHandler is a webapp2 handler that is usefull while developing locally, there is no need for it when the application is live.




[1]: <https://cloud-storage-test-1350.appspot.com/upload/example>
[2]: <https://storage.googleapis.com/cst-003644/example>
[3]: <https://cloud-storage-test-1350.appspot.com/upload/this/is/another/subpath>
[4]: <https://cloud.google.com/appengine/docs/python/quickstart>
[5]: <http://stackoverflow.com/questions/20121031/how-can-i-access-files-from-a-google-cloud-storage-bucket-from-a-browser>
