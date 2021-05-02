
import schedule
import time
from datetime import datetime
import os
import urllib.request
import boto3

# # .ENV FILE FOR TESTING
# if os.path.exists('.env'):
#     from dotenv import load_dotenv
#     load_dotenv()

# GLOBALS
RUNMINS = int(os.environ.get('RUNMINS', 1))
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID','')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
ROUTE53_HOSTED_ZONE_ID = os.environ.get('ROUTE53_HOSTED_ZONE_ID', '')
RECORD_NAME = os.environ.get('RECORD_NAME', '')
RECORD_TYPE = os.environ.get('RECORD_TYPE', '')
RECORD_TTL = int(os.environ.get('RECORD_TTL', 300))
PROVIDER = os.environ.get('PROVIDER', '')

IPADDRESSURL = "http://diagnostic.opendns.com/myip"

#PROVIDER GLOBALS
#ROUTE53
R53_CLIENT = boto3.client('route53', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
#FUTURE

previous_ip = '0.0.0.0'
current_ip = '0.0.0.0'
update_pending = False

def get_my_ip():
    with urllib.request.urlopen(IPADDRESSURL) as f:
        try:
            my_ip = f.read().decode('utf-8')
        except:
            my_ip='0.0.0.0'
    return my_ip

def update_r53(**kwargs):
    global update_pending
    response = R53_CLIENT.change_resource_record_sets(
        HostedZoneId=ROUTE53_HOSTED_ZONE_ID,
        ChangeBatch= {
                        'Comment': 'Dynamic DNS Update',
                        'Changes': [
                            {
                             'Action': 'UPSERT',
                             'ResourceRecordSet': {
                                 'Name': RECORD_NAME,
                                 'Type': RECORD_TYPE,
                                 'TTL': RECORD_TTL,
                                 'ResourceRecords': [{'Value': current_ip}]
                            }
                        }]
        })
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("{} INFO: Route 53 record updated succesfully".format(str(datetime.now())))
        update_pending = False
    else:
        print("{} ERROR: Unable to update R53 retrying".format(str(datetime.now())))
        update_pending = True
    return


def do_it():
    global current_ip
    global previous_ip
    previous_ip = current_ip
    current_ip = get_my_ip()
    if current_ip == previous_ip:
        print("{} INFO: IP has not changed ({})".format(str(datetime.now()), current_ip))
        if update_pending == True:
            print("{} INFO: Route53 update pending, retrying ({})".format(str(datetime.now()), current_ip))
            if PROVIDER == 'ROUTE53':
                update_r53()
    else:
        print("{} INFO: Changing IP {} to {}".format(str(datetime.now()), current_ip, RECORD_NAME))
        if PROVIDER == 'ROUTE53':        
            update_r53()


def main():
    ''' Main entry point of the app '''
    do_it()
    schedule.every(RUNMINS).minutes.do(do_it)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    ''' This is executed when run from the command line '''
    main()