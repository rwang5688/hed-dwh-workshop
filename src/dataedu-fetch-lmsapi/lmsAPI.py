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


from datetime import datetime
from botocore.exceptions import ClientError
import boto3
import base64
import json
import csv
import urllib.request
import os

import logging
logger = logging.getLogger(__name__)

ssm_client = boto3.client('ssm')
ssm_lms_parameter = '/dataedu/lms-demo/state'
lmsTableListCSVFile = "./data/tables.csv"


def getLMSParameter():
    parameter = ssm_client.get_parameter(Name=ssm_lms_parameter)
    return json.loads(parameter ['Parameter']['Value'])

lmsParms = getLMSParameter()

    
def putLMSParameter(parmJSON):
    response = ssm_client.put_parameter(
        Name=ssm_lms_parameter,
        Value=json.dumps(parmJSON),
        Overwrite=True
    )


def getFileURLsForDate(process_date, initial_load=False):
    urlList = list()
    
    inventory = getInventoryList()
    for item in inventory:
        if (initial_load and isPriorTo(item[0],process_date)) or (item[0] == process_date):
            urlList.append("https://{}/{}/{}".format(lmsParms["base_url"], lmsParms["version"],item[1]))

    return urlList
    
    
inventoryCSVFile = "./data/inventory.csv"
def getInventoryList():
    inventoryURL = "{}/{}/inventory.csv".format(lmsParms["base_url"], lmsParms["version"])
    
    try:
        print("getting remote inventory list at {}".format(inventoryURL))
        local_filename, headers = urllib.request.urlretrieve("https://{}".format(inventoryURL))
        print("got inventory locally to {}".format(local_filename))
    except:
        local_filename = inventoryCSVFile
    
    with open(local_filename, 'r') as csvf:
        data = [tuple(line) for line in csv.reader(csvf, delimiter=",")]
    
    if "/tmp" in local_filename:
        print("removing tmp file")
        os.remove(local_filename)
    return data[1:]

def isPriorTo(datestring1, datestring2):
    d1 = datetime.strptime(datestring1, '%Y-%m-%d')
    d2 = datetime.strptime(datestring2, '%Y-%m-%d')
    
    return d1 <= d2