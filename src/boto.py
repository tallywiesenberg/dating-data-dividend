import boto3
from botocore.exceptions import NoCredentialsError
from decouple import config

ACCESS_KEY = config('AWS_ACCESS_KEY')
SECRET_KEY = config('oOvSNsUjQ7fdo/NcFJi3WIEfWGXqV/Zm5W1X3XfD')

def upload_to_s3(local_file_name, bucket, s3_file_name):
    s3 = boto3.client('s3',
                      aws_access_key=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file_name, bucket, s3_file_name)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False