"""
Objective: checks to see that there's an email subscription to our admin

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
########################## ac7-16-1-Email-subscriptions-use-admin.py ##############################
### Audit check 7.16.1 Email notification messaging must only be sent to admin email address.
###
### Usage:
### python ac7-16-1-Email-subscriptions-use-admin.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    sns = boto3.client('sns', region_name=args.region)
    paginator = sns.get_paginator('list_subscriptions')
    page_iter = paginator.paginate()
    print("Checking for subscriptions that use email endpoint protocol...")
    foundSNS = False
    for page in page_iter:
        for p in page['Subscriptions']:
            foundSNS = True
            sub_arn = p['SubscriptionArn']
            topic_arn = p['TopicArn']
            endpoint = p['Endpoint']
            protocol = p['Protocol']
            if protocol == "email":
                if "@made-up-company.com" in endpoint or "@am.made-up-company.com" in endpoint:
                    print("\tPASS: %s is a valid email and endpoint for SNS subscription. Subscription ARN: %s" % (endpoint, sub_arn))
                else:
                    print("\tFAIL: %s does not appear to be a valid email. Subscription ARN: %s" % (endpoint, sub_arn))
    
    if foundSNS == False:
        print("\tFAIL: @made-up-company.com does not appear to be a valid email used in an SNS subscription.")


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
