import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ttaylor-med-api-3285443a6f89.json'

storage_client = storage.Client()

bName = ''

bucket = storage_client.bucket(bName)
bucket.location = 'US' 
bucket = storage_client.create_bucket(bucket)

print(vars(bucket))