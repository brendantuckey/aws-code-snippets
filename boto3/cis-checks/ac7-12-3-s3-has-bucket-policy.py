"""
Objective: Checks S3 buckets have a bucket policy.

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
########################## ac7-12-3-s3-has-bucket-policy.py ##############################
### Audit check 7.12.5 Bucket policies must be used to manage access/permissions for S3 buckets.
###
### Usage:
### python ac7-12-3-s3-has-bucket-policy.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()['Buckets']
    for b in buckets:
        name = b['Name']
        print("Checking bucket policy for %s" % name)
        try:
            policy = s3.get_bucket_policy(Bucket=name)['Policy']
            if policy:
                print("\tPASS: Bucket %s has a policy defined." % name)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "NoSuchBucketPolicy":
                print("\tFAIL: No bucket policy defined for %s" % name)
            else:
                print("\tUnexpected error: %s" % e)
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
