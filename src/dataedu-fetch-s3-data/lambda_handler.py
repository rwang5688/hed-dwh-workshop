# MIT No Attribution

# Copyright (c) 2021 Amazon Web Services (AWS)

# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import logging
from io import BytesIO
from pprint import pprint

import boto3
import requests
from smart_open import open

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    file_url = event['file_url']
    s3_bucket = event['s3_bucket']
    key = event['key']

    chunk_size = 1024*1024*8

    logger.info('fetching {} to {}'.format(file_url, key))

    s3 = boto3.client('s3')
    obj_list = s3.list_objects_v2(Bucket=s3_bucket, Prefix=key)

    if obj_list.get('KeyCount', 0) > 0:
        logger.warn('trying to download {} but it already exists -- skipping'.format(key))
        return({
            'message': 'key {} already exists - skipping'.format(key)
        })

    with open('s3://{}/{}'.format(s3_bucket, key), 'wb', ignore_ext=True) as fout:
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk: # filter out keep-alive new chunks
                    fout.write(chunk)

    return {
        'statusCode': 200,
    }
