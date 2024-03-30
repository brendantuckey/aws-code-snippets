"""
Objective: Checks ALBs Listeners.

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
########################## ac7-13-2-albs-have-https-ssl-cert.py ##############################
### Audit check 7.13.2 All Application Load Balancers (ALB) must use HTTPS listeners and
### have a trusted and verifiable SSL certificate configured.
###
### Usage:
### python ac7-13-2-albs-have-https-ssl-cert.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    elb = boto3.client('elbv2', region_name=args.region)
    albs = elb.describe_load_balancers()['LoadBalancers']
    lb_identified = False
    for alb in albs:
        lb_name = alb['LoadBalancerName']
        lb_type = alb['Type']
        lb_arn = alb['LoadBalancerArn']
        print("Checking load balancer %s for listeners and SSL certificates..." % lb_name)
        if lb_type == 'application' or lb_type == 'network':
            listeners = elb.describe_listeners(LoadBalancerArn=lb_arn)['Listeners']
            for listener in listeners:
                listener_arn = listener['ListenerArn']
                protocol = listener['Protocol']
                port = listener['Port']
                print("\tType: %s, Protocol:Port--> %s:%s" % (lb_type, protocol, port) )
                try:
                    ssl_certs = elb.describe_listener_certificates(ListenerArn=listener_arn)['Certificates']
                    for cert in ssl_certs:
                        print("\tListener configured with %s protocol on port %s. Certificate ARN for Application Load Balancer %s" % (protocol, port, cert['CertificateArn']))
                except KeyError:
                    print("\tNo certificates configured for this listener.")
            lb_identified = True
        
        if not lb_identified:
            print("\tNo application or Network load balancers for this account.")



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
