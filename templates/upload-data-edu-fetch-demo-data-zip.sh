#!/bin/bash
export AWS_REGION='us-west-2'

export SOURCE_CODE_BUCKET_NAME_PREFIX='ee-assets-prod-9132e5491bd44c56aaaaefc3e91b6aa8-'
export SOURCE_MODULE_VERSION_PREFIX='modules/cfdd4f678e99415a9c1f11342a3a9887/v1/'

rm -rf ./zip && mkdir zip
cp -r ./data_edu_fetch_demo_data/* ./zip
cd ./zip
git archive -o data_edu_fetch_demo_data.zip HEAD data_edu_fetch_demo_data.py s3_util.py requirements.txt
aws s3 cp data_edu_fetch_demo_data.zip \
    s3://${SOURCE_CODE_BUCKET_NAME_PREFIX}${AWS_REGION}/${SOURCE_MODULE_VERSION_PREFIX}lambda/
cd ..
