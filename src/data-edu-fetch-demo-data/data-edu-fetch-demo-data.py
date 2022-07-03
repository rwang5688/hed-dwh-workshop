import s3_util


def main():
    # Start
    print('\nStarting data-edu-fetch-demo-data.py ...')

    # We would normally set these via config file or env vars
    # Hard coding these to keep the demo simple
    profile_name = 'default'
    region_name = 'us-east-1'

    # Source bucket name is specific to Data EDU Immersion Day workshop
    source_bucket_name = 'ee-assets-prod-us-west-2'
    sis_demo_source_prefix = 'modules/cfdd4f678e99415a9c1f11342a3a9887/v1/mockdata/sis_demo/'
    lms_demo_source_prefix = 'modules/cfdd4f678e99415a9c1f11342a3a9887/v1/mockdata/lms_demo/v1/'

    # Dest_bucket_name is specific to wangrob-migrations-sandbox-07
    dest_bucket_name = 'data-edu-raw-6114e92354234c16b7d90ca97ccc8fc6'
    sis_demo_dest_prefix = 'sis_demo/'
    lms_demo_dest_prefix = 'lms_demo/'

    # Get list of SIS demo source objects
    sis_demo_source_object_names = s3_util.get_s3_object_names(profile_name, region_name, \
        source_bucket_name, sis_demo_source_prefix)
    num_sis_demo_source_object_names = len(sis_demo_source_object_names)

    print("sis_demo_source_object_names: ")
    print(sis_demo_source_object_names)
    print("Total # of SIS demo source objects: %d" % num_sis_demo_source_object_names)

    # Copy to SIS demo dest objects
    sis_demo_dest_object_names = s3_util.copy_s3_objects(profile_name, region_name, \
        source_bucket_name, sis_demo_source_prefix, sis_demo_source_object_names, \
        dest_bucket_name, sis_demo_dest_prefix)
    num_sis_demo_dest_object_names = len(sis_demo_dest_object_names)

    print("sis_demo_dest_object_names: ")
    print(sis_demo_dest_object_names)
    print("Total # of SIS demo dest objects: %d" % num_sis_demo_dest_object_names)

    # Get list of LMS demo source objects
    lms_demo_source_object_names = s3_util.get_s3_object_names(profile_name, region_name, \
        source_bucket_name, lms_demo_source_prefix)
    num_lms_demo_source_object_names = len(lms_demo_source_object_names)

    print("lms_demo_source_object_names: ")
    print(lms_demo_source_object_names)
    print("Total # of LMS demo source objects: %d" % num_lms_demo_source_object_names)
    
    # Copy to LMS demo dest objects
    lms_demo_dest_object_names = s3_util.copy_s3_objects(profile_name, region_name, \
        source_bucket_name, lms_demo_source_prefix, lms_demo_source_object_names, \
        dest_bucket_name, lms_demo_dest_prefix)
    num_lms_demo_dest_object_names = len(lms_demo_dest_object_names)

    print("lms_demo_dest_object_names: ")
    print(lms_demo_dest_object_names)
    print("Total # of LMS demo dest objects: %d" % num_lms_demo_dest_object_names)

    # End
    print('\n... Thaaat\'s all, Folks!')


if __name__ == '__main__':
    main()

