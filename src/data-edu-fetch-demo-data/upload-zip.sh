#!/bin/bash
export AWS_REGION='us-east-1'

export SOURCE_CODE_BUCKET_NAME_PREFIX='ee-assets-prod-6114e92354234c16b7d90ca97ccc8fc6-'
export SOURCE_MODULE_VERSION_PREFIX='modules/cfdd4f678e99415a9c1f11342a3a9887/v1/'

rm -rf ./dist && mkdir dist
cp -r ./data_edu_fetch_demo_data/* ./dist
cd ./dist
git archive -o data_edu_fetch_demo_data.zip data_edu_fetch_demo_data.py s3_util.py requirements.txt
aws s3 cp data_edu_fetch_demo_data.zip \
    s3://${SOURCE_CODE_BUCKET_NAME_PREFIX}${AWS_REGION}/${SOURCE_MODULE_VERION_PREFIX}/lambda/
cd ..
