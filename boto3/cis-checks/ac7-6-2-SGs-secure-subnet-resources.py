"""
Objective: Checks Security Groups are set up.

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
################ ac7-6-2-SGs-secure-subnet-resources.py ##################
### Audit check 7.6.2 Security Groups should be used as default minimum to secure
### resources in a subnet.
###
###
### Usage:
### python ac7-6-2-SGs-secure-subnet-resources.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    ec2 = boto3.client('ec2', region_name=args.region)
    subnets = ec2.describe_subnets()['Subnets']
    for s in subnets:
        subnet_id = s['SubnetId']
        print("Resources in subnet %s...\n\n" % subnet_id)
        net_interface = ec2.describe_network_interfaces(Filters=[{'Name' : 'subnet-id', 'Values': [subnet_id]}])['NetworkInterfaces']
        for resource in net_interface:
            resource_name = resource['NetworkInterfaceId']
            sec_groups = resource['Groups']
            print("\tResource %s" % resource_name)
            if sec_groups:
                print("\t\tSecurity Groups are configured:")
                for sg in sec_groups:
                    print("\t\t\t" + sg['GroupName'])
            else:
                print("\t\tWARN: No Secuirty Groups attached to this resource")
            print("-" * 80)
        print("#" * 80)


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
