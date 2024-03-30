"""
Objective: Discover's whetther a Default VPC still exists. It shouldn't as is insecure.

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
################ ac7-5-3-VPC-created.py ##################
### Audit check 7.5.3 - For new accounts using default VPC is not permitted for use as default
### settings are insecure. A new VPC must be created from scratch.
###
###
### Usage:
### python ac7-5-3-VPC-created.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    ec2 = boto3.client('ec2', region_name=args.region)
    default_vpc = ec2.describe_vpcs(Filters=[{'Name': 'isDefault','Values': ['true']}])['Vpcs']
    if default_vpc:
        for vpc in default_vpc:
            vpc_id = vpc['VpcId']
            print("Default VPC found: %s " % vpc_id)
    else:
        print("No Default VPC found.")




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

