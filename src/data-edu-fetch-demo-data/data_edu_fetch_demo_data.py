import os
import s3_util

def get_env_vars():
    global profile_name
    global region_name

    global source_data_bucket_name_prefix
    global source_module_version_prefix
    global sis_demo_mock_data_prefix
    global lms_demo_mock_data_prefix

    global raw_data_bucket_name
    global sis_demo_raw_data_prefix
    global lms_demo_raw_data_prefix

    profile_name = 'default'
    region_name = os.environ['AWS_REGION']

    source_data_bucket_name_prefix = os.environ['SOURCE_DATA_BUCKET_NAME_PREFIX']
    source_module_version_prefix = os.environ['SOURCE_MODULE_VERSION_PREFIX']
    sis_demo_mock_data_prefix = os.environ['SIS_DEMO_MOCK_DATA_PREFIX']
    lms_demo_mock_data_prefix = os.environ['LMS_DEMO_MOCK_DATA_PREFIX']
    raw_data_bucket_name = os.environ['RAW_DATA_BUCKET_NAME']
    sis_demo_raw_data_prefix = os.environ['SIS_DEMO_RAW_DATA_PREFIX']
    lms_demo_raw_data_prefix = os.environ['LMS_DEMO_RAW_DATA_PREFIX']

    # DEBUG
    print("get_env_vars:")
    print("profile_name: %s" % (profile_name))
    print("region_name: %s" % (region_name))
    print("source_data_bucket_name_prefix: %s" % (source_data_bucket_name_prefix))
    print("source_module_version_prefix: %s" % (source_module_version_prefix))
    print("sis_demo_mock_data_prefix: %s" % (sis_demo_mock_data_prefix))
    print("lms_demo_mock_data_prefix: %s" % (lms_demo_mock_data_prefix))
    print("raw_data_bucket_name: %s" % (raw_data_bucket_name))
    print("sis_demo_raw_data_prefix: %s" % (sis_demo_raw_data_prefix))
    print("lms_demo_raw_data_prefix: %s" % (lms_demo_raw_data_prefix))


def lambda_handler(event, context):
    # start
    print('\nStarting data-edu-fetch-demo-data.lambda_handler ...')
    print("event: %s" % (event))
    print("context: %s" % (context))

    # get environment variables
    get_env_vars()

    # assemble source data bucket name and object name prefixes
    source_data_bucket_name = source_data_bucket_name_prefix + region_name
    sis_demo_source_data_prefix = source_module_version_prefix + sis_demo_mock_data_prefix
    lms_demo_source_data_prefix = source_module_version_prefix + lms_demo_mock_data_prefix

    # get SIS demo mock data objects
    sis_demo_source_object_names = s3_util.get_s3_object_names(profile_name, region_name, \
        source_data_bucket_name, sis_demo_source_data_prefix)
    num_sis_demo_source_object_names = len(sis_demo_source_object_names)

    print("sis_demo_source_object_names: ")
    print(sis_demo_source_object_names)
    print("Total # of SIS demo source objects: %d" % num_sis_demo_source_object_names)

    # copy to SIS demo raw data objects
    sis_demo_dest_object_names = s3_util.copy_s3_objects(profile_name, region_name, \
        source_data_bucket_name, sis_demo_source_data_prefix, sis_demo_source_object_names, \
        raw_data_bucket_name, sis_demo_raw_data_prefix)
    num_sis_demo_dest_object_names = len(sis_demo_dest_object_names)

    print("sis_demo_dest_object_names: ")
    print(sis_demo_dest_object_names)
    print("Total # of SIS demo dest objects: %d" % num_sis_demo_dest_object_names)

    # get LMS demo mock data objects
    lms_demo_source_object_names = s3_util.get_s3_object_names(profile_name, region_name, \
        source_data_bucket_name, lms_demo_source_data_prefix)
    num_lms_demo_source_object_names = len(lms_demo_source_object_names)

    print("lms_demo_source_object_names: ")
    print(lms_demo_source_object_names)
    print("Total # of LMS demo source objects: %d" % num_lms_demo_source_object_names)
    
    # copy to LMS demo raw data objects
    lms_demo_dest_object_names = s3_util.copy_s3_objects(profile_name, region_name, \
        source_data_bucket_name, lms_demo_source_data_prefix, lms_demo_source_object_names, \
        raw_data_bucket_name, lms_demo_raw_data_prefix)
    num_lms_demo_dest_object_names = len(lms_demo_dest_object_names)

    print("lms_demo_dest_object_names: ")
    print(lms_demo_dest_object_names)
    print("Total # of LMS demo dest objects: %d" % num_lms_demo_dest_object_names)

    # end
    print('\n... Thaaat\'s all, Folks!')


if __name__ == '__main__':
    event = {}
    context = {}
    lambda_handler(event, context)

