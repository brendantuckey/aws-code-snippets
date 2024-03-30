"""
Objective: Checks ELB access logging is enabled and sent to a dedicated S3 bucket

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
########################## ac7-13-5-ELB-access-logging-enabled.py ##############################
### Audit check 7.13.5 ELB access logging must be enabled and sent to a dedicated
### Information Security S3 bucket.
###
### Usage:
### python ac7-13-5-ELB-access-logging-enabled.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    elb = boto3.client('elbv2', region_name = args.region)
    elbs = elb.describe_load_balancers()['LoadBalancers']
    for elb_details in elbs:
        elb_name = elb_details['LoadBalancerName']
        elb_arn = elb_details['LoadBalancerArn']
        lb_attributes = elb.describe_load_balancer_attributes(LoadBalancerArn=elb_arn)['Attributes']
        
        for attributes in lb_attributes:
            if attributes['Key'] == "access_logs.s3.enabled":
                s3_access_log_enabled = attributes['Value']

        if s3_access_log_enabled == "true":
            print("PASS: ELB %s has S3 access logs enabled" % elb_name)
        else:
            print("FAIL: No S3 access logs have been enabled for %s." % elb_name)



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
