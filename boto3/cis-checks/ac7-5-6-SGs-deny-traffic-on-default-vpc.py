"""
Objective: Checks inbound and outbound traffic on default VPC.

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
################ ac7-5-6-SGs-deny-traffic-on-default-vpc.py ##################
### Audit check 7.5.6 - Default VPC security groups must be updated to deny all inbound and
### outbound traffic.
###
###
### Usage:
### python ac7-5-6-SGs-deny-traffic-on-default-vpc.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    ec2 = boto3.client('ec2', region_name=args.region)
    sec_groups = ec2.describe_security_groups()['SecurityGroups']
    for sg in sec_groups:
        sg_name = sg['GroupName']
        if sg_name == 'default':
            ingress_permissions = sg['IpPermissions']
            egress_permissions = sg['IpPermissionsEgress']
            if ingress_permissions or egress_permissions:
                json_ingress = json.dumps(ingress_permissions, indent=4)
                json_egress = json.dumps(egress_permissions, indent=4)
                if ingress_permissions:
                    print("Ingress rule defined for Security Group %s:" % sg_name)
                    print(json_ingress)
                if egress_permissions:
                    egress_cidrs = [egress_permission['IpRanges'][0]['CidrIp'] for egress_permission in egress_permissions]
                    if '0.0.0.0/0' in egress_cidrs:
                        print("Egress rule defined for Security Group %s and CidrIp 0.0.0.0/0!!!:" % sg_name)
                    else:
                        print("Egress rule defined for Security Group %s:" % sg_name)
                    print(json_egress)
            else:
                print("No rules are defined for the default Security Group")


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
