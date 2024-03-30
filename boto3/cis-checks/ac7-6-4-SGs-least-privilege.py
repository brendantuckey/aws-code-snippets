"""
Objective: Describes all Security goups for checking for least privilege.

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
################ ac7-6-4-SGs-least-privilege.py ##################
### Audit check 7.6.4 Security Groups must be configured based on a least privilege (explicit
### allow) for incoming and outgoing traffic.
### Note that additionally "Open Internet" CidrIP usage is highlighted
###
###
### Usage:
### python ac7-6-4-SGs-least-privilege.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def highlight_cider_ip(rule):
    if any("0.0.0.0/0" in ip_range.get("CidrIp", "") for ip_range in rule.get("IpRanges", [])):
        return "\033[1;31m" + json.dumps(rule, indent=4) + "\033[0m"  # ANSI escape code for red color
    else:
        return json.dumps(rule, indent=4)
        
def main(args):
    ec2 = boto3.client('ec2', region_name=args.region)
    sec_groups = ec2.describe_security_groups()['SecurityGroups']
    for s in sec_groups:
        sg_name = s['GroupName']
        permissions = s['IpPermissions']
        print("\n\nSecurity group %s..." % sg_name)
        for rule in permissions:
            policy_json = highlight_cider_ip(rule)
            print(policy_json)



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
