"""
Objective: Find unused EBS drives.

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
########################## ac7-11-14-unused-ebs-finder.py ##############################
### Audit check 7.11.14 Unused data stores (ie: Elastic Block Stores (EBS)) must be
### removed when no longer needed or archived.
###
###
### Usage:
### python ac7-11-14-unused-ebs-finder.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    ec2 = boto3.client('ec2', region_name=args.region)
    #volumes = ec2.describe_volumes(Filter=['Name' : 'attachment.status', 'Values' : ['attached']])
    volumes = ec2.describe_volumes(Filters=[{'Name' : 'status', 'Values' : ['available']}])['Volumes']
    print("Searching for detached volumes...")
    if volumes:
        for vol in volumes:
            vol_id = vol['VolumeId']
            attachment = vol['Attachments']
            print("ID: %s is detached... Attachments: %s" % (vol_id, attachment))
    else:
        print("No detached volumes found.")


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