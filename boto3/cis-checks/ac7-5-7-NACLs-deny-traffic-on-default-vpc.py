"""
Objective: Checks inbound and outbound traffic on default VPC NACLs.

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
################ ac7-5-6-NACLs-deny-traffic-on-default-vpc.py ##################
### Audit check 7.5.7 Default VPC NACL must be configured to deny all inbound and
### outbound traffic.
###
###
### Usage:
### python ac7-5-6-NACLs-deny-traffic-on-default-vpc.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    ec2 = boto3.client('ec2', region_name=args.region)
    default_nacl = ec2.describe_network_acls(Filters=[{'Name' : 'default', 'Values' : ['true']}])['NetworkAcls']
    for nacl in default_nacl:
        print("Default NACL %s entries:" % nacl['NetworkAclId'])
        if nacl['Entries']:
            for entry in nacl['Entries']:
                if entry['Egress']:
                    traffic_flow = "EGRESS Rule"
                else:
                    traffic_flow = "INGRESS Rule"
                if entry['RuleAction'] != 'deny':
                    print("\tAn ALLOW rule has been found. Rule # %d (%s)" % (entry['RuleNumber'], traffic_flow))
        else:
            print("\tAll rule entries (inbound and outbound) for the default NACL are set to DENY.")


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
