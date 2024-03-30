"""
Objective: Checks If any of the AMIs you're using are public.

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

ARG_HELP = """
########################## ac7-11-1-AMIs-not-public.py ##############################
### Audit check 7.11.1 Use of public Amazon Machine Images (AMIs) is not permitted
### unless provided directly by AWS or approved third parties.
###
###
### Usage:
### python ac7-11-1-AMIs-not-public.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    ec2 = boto3.client('ec2', region_name=args.region)
    instances = ec2.describe_instances()['Reservations']
    for instance in instances:
        #print(instance)
        for i in instance['Instances']:
            image_id = i['ImageId']
            instance_id = i['InstanceId']
            amis = ec2.describe_images(Filters = [{'Name' : 'image-id', 'Values' : [image_id]}])['Images']
            for ami in amis:
                if ami['Public']:
                    print("Instance %s is using public AMI. Image name: %s ImageId: %s" % (instance_id, ami['Name'], image_id))


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
