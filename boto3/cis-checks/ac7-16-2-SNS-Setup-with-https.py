"""
Objective: checks to see that SNS is set up with HTTPS protocol

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
########################## ac7-16-2-SNS-Setup-with-https.py ##############################
### Audit check 7.16.2 AWS SNS subscriptions must be configured with the HTTPS protocol.
###
### Usage:
### python ac7-16-2-SNS-Setup-with-https.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    sns = boto3.client('sns', region_name=args.region)
    sns_subscriptions = sns.list_subscriptions()['Subscriptions']
    if len(sns_subscriptions) == 0:
        print("No SNS Subscriptions found")
    else:
        for sns_subscription in sns_subscriptions:
            print("SNS Subscription %s details...\n" % sns_subscription['SubscriptionArn'])
            if sns_subscription['Protocol'] == 'https':
                print("\tPASS: SNS Subscription using HTTPS. Endpoint: %s " % sns_subscription['Endpoint'])
            else:
                print("\tFAIL: SNS Subscription using %s. Endpoint: %s " % (sns_subscription['Protocol'], sns_subscription['Endpoint']))


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
