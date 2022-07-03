# MIT No Attribution

# Copyright 2021 Amazon Web Services (AWS)

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
from datetime import datetime, timedelta
import boto3
import lmsAPI

import logging
logger = logging.getLogger(__name__)

events_client = boto3.client('events')

def convertURLsToS3Prefixes(urlList):
    prefixes = list()
    base_s3_prefix   = lmsAPI.lmsParms["base_s3_prefix"]
    for url in urlList:
        s3Prefix = url.replace("https://{}/{}/".format(lmsAPI.lmsParms["base_url"], lmsAPI.lmsParms["version"]), "")
        prefixes.append("{}/{}".format(base_s3_prefix, s3Prefix))
        
    return prefixes

def lambda_handler(event, context):
    lmb = boto3.client('lambda')
    print(event)


    print("starting parms {}".format(json.dumps(lmsAPI.lmsParms)))
    current_date = lmsAPI.lmsParms["current_date"]

    print(current_date)
    
    #
    #  If CURRENT DATE > today's date OR
    #  param "disable_api" = 1
    #  Execute disable API function
    
    if isFutureDate(current_date):
        print("{} is future date".format(current_date))

    if "disable_api" in lmsAPI.lmsParms or isFutureDate(current_date):
        print("disabling event rule & returning")
        response = events_client.disable_rule(Name='dataedu-lmsapi-sync')
        
        print("event rule disabled, retu")
        return {
            'statusCode': 200,
            'body': json.dumps('LMS API being disabled')
        }
        
    target_s3_bucket = lmsAPI.lmsParms["target_bucket"]
    perform_initial_load = lmsAPI.lmsParms["perform_initial_load"]
    
    urlList = lmsAPI.getFileURLsForDate(current_date, initial_load=(perform_initial_load=="1"))
    print(urlList)
    
    s3PrefixList = convertURLsToS3Prefixes(urlList)
    print(s3PrefixList)
    
    # Invoke function again fo reach data file to obtain
    i = 0
    for prefix in s3PrefixList:
        payload = {}
        payload["file_url"] = urlList[i]
        payload["s3_bucket"] = target_s3_bucket
        payload["key"] = prefix
        
        i = i + 1
        print("INVOKING fetch_function payload({})".format(payload))
        status = lmb.invoke(
                FunctionName='dataedu-fetch-s3-data',
                InvocationType='Event',
                Payload=json.dumps(payload),
                )
                
    print("Updating lmsParms")
    next_date = calcNextDate(lmsAPI.lmsParms["current_date"])
    lmsAPI.lmsParms["current_date"] = dateString(next_date)
    lmsAPI.lmsParms["perform_initial_load"] = "0"
    lmsAPI.putLMSParameter(lmsAPI.lmsParms)
    print("ending parms {}".format(json.dumps(lmsAPI.lmsParms)))


    return {
        'statusCode': 201,
        'body': json.dumps('LMS API automation function completed with STATUS = SUCCESS')
    }





def calcNextDate(current_date_string):
    next_date = datetime.strptime(current_date_string, '%Y-%m-%d') + timedelta(days = 7)
    return next_date
    
def dateString(dateObj):
    return dateObj.strftime('%Y-%m-%d')
    

def isFutureDate(current_date_string):
    cd = datetime.strptime(current_date_string, '%Y-%m-%d')
    return cd > datetime.now()