"""
Objective: Checks ELBs Protocol and Port.

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
########################## ac7-13-3-elbs-have-tls-protocol.py ##############################
### Audit check 7.13.3 All Network ELB listeners should be configured to use the TLS
### protocol when architecturally appropriate.
###
### Usage:
### python ac7-13-3-elbs-have-tls-protocol.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    elbv2 = boto3.client('elbv2', region_name=args.region)
    elbs = elbv2.describe_load_balancers()['LoadBalancers']
    if elbs:
        for elb in elbs:
            elb_arn = elb['LoadBalancerArn']
            elb_type = elb['Type']
            elb_name = elb['LoadBalancerName']
            if elb_type == "network":
                print("Retrieving listeners for Network ELB %s..." % elb_name)
                listeners = elbv2.describe_listeners(LoadBalancerArn=elb_arn)['Listeners']
                for l in listeners:
                    listener_arn = l['ListenerArn']
                    port = l['Port']
                    protocol = l['Protocol']
                    print("\tConfigured to use %s protocol on port %d." % (protocol, port))
                    print("\tARN: %s" % (listener_arn))
                print('-' * 80)
    else:
        print("INFO: No ELBs configured for this account.")


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
