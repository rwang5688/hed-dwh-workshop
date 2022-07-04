#!/bin/bash
export AWS_REGION='us-east-1'

export SOURCE_DATA_BUCKET_NAME_PREFIX='ee-assets-prod-'
export SOURCE_MODULE_VERSION_PREFIX='modules/cfdd4f678e99415a9c1f11342a3a9887/v1/'
export SIS_DEMO_MOCK_DATA_PREFIX='mockdata/sis_demo/'
export LMS_DEMO_MOCK_DATA_PREFIX='mockdata/lms_demo/v1/'
export RAW_DATA_BUCKET_NAME='data-edu-raw-6114e92354234c16b7d90ca97ccc8fc6'
export SIS_DEMO_RAW_DATA_PREFIX='sis_demo/'
export LMS_DEMO_RAW_DATA_PREFIX='lms_demo/'

echo "[CMD] python data_edu_fetch_demo_data.py"
python data_edu_fetch_demo_data/data_edu_fetch_demo_data.py

