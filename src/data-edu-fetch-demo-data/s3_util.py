import logging
import boto3
from botocore.exceptions import ClientError


def get_s3_client(profile_name, region_name):
    print('get_s3_client: profile_name=%s, region_name=%s' % (profile_name, region_name))

    session = boto3.Session(profile_name=profile_name)
    s3 = session.client('s3',
        region_name=region_name)
    return s3


def get_s3_object_names(profile_name, region_name, bucket_name, prefix):
    s3_object_names = []

    s3 = get_s3_client(profile_name, region_name)
    if s3 is None:
        print('get_s3_object_names: Failed to get s3 client.')
        return s3_object_names

    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        print('DEBUG: get_s3_object_names: s3.list_objects_v2() response: %s' % (response))
        
        for object in response['Contents']:
            key = object['Key']
            print('get_s3_object_names: key: %s' % (key))
            s3_object_names.append(key)
        
    except ClientError as e:
        logging.error("get_s3_bucket_names: unexpected error: ")
        logging.exception(e)
        return s3_object_names

    return s3_object_names


def copy_s3_objects(profile_name, region_name, \
    source_bucket_name, source_prefix, source_object_names, \
    dest_bucket_name, dest_prefix):
    dest_object_names = []

    s3 = get_s3_client(profile_name, region_name)
    if s3 is None:
        print('copy_s3_objects: Failed to get s3 client.')
        return dest_object_names

    try:
        for source_object_name in source_object_names:
            copy_source = {
                'Bucket': source_bucket_name,
                'Key': source_object_name
            }
            dest_object_name = source_object_name.replace(source_prefix, dest_prefix)

            s3.copy(copy_source, dest_bucket_name, dest_object_name)
            print('DEBUG: copy_s3_objects: dest_object_name: %s' % (dest_object_name))

            dest_object_names.append(dest_object_name)
        
    except ClientError as e:
        logging.error("copy_s3_objects: unexpected error: ")
        logging.exception(e)
        return dest_object_names

    return dest_object_names    

