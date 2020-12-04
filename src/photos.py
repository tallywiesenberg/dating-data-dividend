import logging

import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from .extensions import config
import requests

ACCESS_KEY = config('AWS_ACCESS_KEY')
SECRET_KEY = config('AWS_SECRET_KEY')

client = boto3.client('s3')

class Photos:

    def __init__(self, path_to_photos_parent):
        self.path_to_photos_parent = path_to_photos_parent
        self.bucket = config('BUCKET_NAME')
        self.access_key = ACCESS_KEY
        self.secret_key = SECRET_KEY
        self.client = boto3.client('s3')


    def upload_to_s3(self, local_file_name, s3_file_name=None):
        '''
        :param local_file_name: File to upload
        :param bucket: Bucket to upload to
        :param s3_file_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        '''

        if s3_file_name is None:
            s3_file_name = local_file_name

        try:
            self.client.put_object(Bucket=self.bucket, 
                                   Filename=local_file_name,
                                   Key = local_file_name,
                                   ExtraArgs={'ACL':'public-read'})
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    def get_paths_to_photos(self, username):
        response_dict = self.client.list_objects_v2(
            Bucket = self.bucket,
            Prefix = f's3/user/{username}/',
            MaxKeys = 100,
        )
        child_paths = []
        for dict_ in response_dict['Contents']:
            child_paths.append(dict_['Key'])
        return child_paths
    
    def create_presigned_url(self, user_id, expiration=3600):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        try:
            response = self.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket,
                    'Key': f'user/{user_id}/'},
                ExpiresIn=expiration)
        except ClientError as e:
            logging.error(e)
            return None

        # The response contains the presigned URL
        return response

        