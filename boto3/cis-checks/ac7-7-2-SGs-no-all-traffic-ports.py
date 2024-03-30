"""
Objective: Checks ingress and egress for "All traffic" ports.

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
################ ac7-7-2-SGs-no-all-traffic-ports.py ##################
### Audit check 7.7.2 Security Groups must be used to restrict access to AWS resources
### using inbound and outbound rules that only authorized protocol types, IP
### addresses and ports based on least privilege. The use of "all" protocol types
### must not be used.
###
###
### Usage:
### python ac7-7-2-SGs-no-all-traffic-ports.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    ec2 = boto3.client('ec2', region_name = args.region)
    sec_groups = ec2.describe_security_groups()['SecurityGroups']
    for sg in sec_groups:
        sg_name = sg['GroupName']
        ingress_rules = sg['IpPermissions']
        egress_rules = sg['IpPermissionsEgress']
        print("Checking security group '%s' for ingress and egress rules with ports open to \"ALL\"..." % sg_name)
        all_port = False
        for rule in ingress_rules:
            if rule['IpProtocol'] == '-1':
                print("\tFAIL: ALL Traffic - ALL ports INGRESS rule found.")
                all_port = True
                continue
            from_port = rule['FromPort']
            to_port = rule['ToPort']
            if from_port == '-1' or to_port == '-1':
                print("\tFAIL: ALL Traffic - ALL ports INGRESS rule found.")
                all_port = True
                continue
        if not all_port:
            print("\tPASS: No ALL port ingress rule found.")

        #print("Checking security group %s for egress rules with ports open to \"ALL\"..." % sg_name)
        all_port = False
        for rule in egress_rules:
            if rule['IpProtocol'] == '-1':
                print("\tFAIL: ALL Traffic - ALL ports EGRESS rule found.")
                all_port = True
                continue
            from_port = rule['FromPort']
            to_port = rule['ToPort']
            if from_port == '-1' or to_port == '-1':
                print("\TFAIL: ALL Traffic - ALL ports EGRESS rule found.")
                all_port = True
                continue
        if not all_port:
            print("\tPASS: No ALL port egress rule found in security group.")
        
        print() # Write a blank line to the console


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
