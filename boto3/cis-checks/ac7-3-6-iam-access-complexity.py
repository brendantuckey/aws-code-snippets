"""
Objective: Dumps PasswordPolicy details for an account

Technologies: python, boto3

Related Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html


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
################ ac7-3-6-iam-access-complexity.py ##################
### Audit check 7.3.6 - Access to the AWS Management Console and AWS API by interactive
### IAM accounts requires using a complex password and MFA, based on least
### privilege and job function.
###
###
### Usage:
### python ac7-3-6-iam-access-complexity.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    iam = boto3.client('iam')
    acct_pwd_policy = iam.get_account_password_policy()['PasswordPolicy']
    json_policy = json.dumps(acct_pwd_policy, indent=4)
    print("Account Password Policy for account %s" % args.profile)
    print(json_policy)



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

