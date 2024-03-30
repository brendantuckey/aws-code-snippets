"""
Objective: Checks ingress and egress for default 0.0.0.0/0 rules.

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
################ ac7-7-1-SGs-no-default-rules.py ##################
### Audit check 7.7.1 All Security Groups must not have inbound or outbound rules
### configured by default (ie: default deny), must remove the 0.0.0.0/0 rules.
###
###
### Usage:
### python ac7-7-1-SGs-no-default-rules.py --profile <acct profile name> --region <AWS region name>
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
        print("Checking security group %s for 0.0.0.0/0 ingress rule..." % sg_name)
        quad_zero = False
        for rule in ingress_rules:
            #print("RULE:", rule)
            try:
                ip_ranges = rule['IpRanges']
                from_port = rule['FromPort']
                to_port = rule['ToPort']
            except:
                ip_protocol = rule['IpProtocol']
                quad_zero = True
                if ip_protocol == '-1':
                    print("\tINGRESS RULE FAILED. Default All Traffic Open internet Egress exists")
                else:
                    print("\tINGRESS RULE FAILED. Unsure as to why, please check")
                continue; 
            for cidr_range in ip_ranges:
                cidr = cidr_range['CidrIp']
                if cidr == '0.0.0.0/0':
                    print('\tFAIL: Found 0.0.0.0/0 (From Port: %d To Port: %d) ingress rule' % (from_port, to_port))
                    quad_zero = True
                    continue
        if not quad_zero:
            print("\tPASS: No 0.0.0.0/0 ingress rule found")
        print() # empty line

        print("Checking security group %s for 0.0.0.0/0 egress rule..." % sg_name)
        quad_zero = False
        for rule in egress_rules:
            #print("RULE:", rule)
            try:
                ip_ranges = rule['IpRanges']
                from_port = rule['FromPort']
                to_port = rule['ToPort']
            except:
                ip_protocol = rule['IpProtocol']
                quad_zero = True
                if ip_protocol == '-1':
                    print("\tFAIL: Default All Traffic Open internet Egress exists")
                else:
                    print("\tFAIL: Unsure as to why, please check:")
                continue; 
                    
            for cidr_range in ip_ranges:
                cidr = cidr_range['CidrIp']
                if cidr == '0.0.0.0/0':
                    print('\tFAIL: Found 0.0.0.0/0 (From Port: %d To Port %d) egress rule' % (from_port, to_port))
                    quad_zero = True
                    continue
        if not quad_zero:
            print("\tPASS: No 0.0.0.0/0 egress rule found")
        print() # empty line

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
