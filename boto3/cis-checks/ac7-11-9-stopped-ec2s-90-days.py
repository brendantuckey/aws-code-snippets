"""
Objective: Checks for any EC2s not used for 90 days.

Technologies: python, boto3

Related Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html


To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/cis-checks
Updated: 3/29/2024

"""

#!/usr/bin/python3
import sys
import boto3
import argparse
import configparser
import json
import botocore.exceptions
import traceback
from datetime import datetime

ARG_HELP = """
########################## ac7-11-9-stopped-ec2s-90-days.py ##############################
### Audit check 7.11.9 EC2 instances which have been inactive (in a stopped or powered off
### state) for more than 90 days must be deleted.
###
###
### Usage:
### python ac7-11-9-stopped-ec2s-90-days.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    ec2 = boto3.client('ec2', region_name=args.region)
    reservations = ec2.describe_instances()['Reservations']
    current_date = datetime.now()
    for res in reservations:
        instances = res['Instances']
        for i in instances:
            instance_id = i['InstanceId']
            state = i['State']['Name']
            if state in ['stopped', 'terminated']:
                transition_reason = i['StateTransitionReason']
                print("Instance %s is currently in the %s state." % (instance_id, state))
                print(transition_reason)
                
                try:
                    # Extract the date from the transition_reason, if available
                    date_str = transition_reason.split("(")[-1].split(")")[0].strip()
                    if date_str:
                        transition_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %Z")
                        days_difference = (current_date - transition_date).days
                        print("Number of days since last initiated: %d" % days_difference)
                except:
                    print("Unable to determine number of days")
                print('-' * 80)

if __name__ == '__main__':
    try:
        args = argparse.ArgumentParser(description=ARG_HELP, formatter_class=argparse.RawTextHelpFormatter, usage=argparse.SUPPRESS)
        args.add_argument('--region','-r', default='us-east-1', help="AWS region name (Default: us-east-1)")
        args.add_argument('--profile','-p', dest='profile', type=str, default="default", help="Profile to use (Default: default)")
        args.add_argument('--verbose','-v', dest='verbose', action='store_true', help="Show verbose output of program")
        args = args.parse_args()
        print(ARG_HELP)
        print("Running checks on account: %s in region %s...\n\n" % (args.profile, args.region))
        # Launch Main
        main(args)
    except Exception as e:
        print("Main exception: ", e)
        traceback.print_exc()
