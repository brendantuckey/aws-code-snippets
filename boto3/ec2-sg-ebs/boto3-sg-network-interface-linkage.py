"""
List all network interfaces and their associated security groups 

Technologies: python, boto3

Documentation
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_security_group.html

Run in Cloud 9:
    python3 boto3-create-security-group.py
OR
    Run button from code editor

Author: Brendan Tuckey
Repo location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/25/2024
"""

import boto3

def get_security_groups_for_network_interfaces():
    ec2 = boto3.client('ec2')
    
    # get all network interfaces
    response = ec2.describe_network_interfaces()
    
    # Iterate through each network interface
    for network_interface in response['NetworkInterfaces']:
        interface_id = network_interface['NetworkInterfaceId']
        security_groups = network_interface['Groups']
        
        # Print the network interface ID and associated security groups
        print(f"Network Interface ID: {interface_id}")
        print("Associated Security Groups:")
        for group in security_groups:
            group_id = group['GroupId']
            group_name = ec2.describe_security_groups(GroupIds=[group_id])['SecurityGroups'][0]['GroupName']
            print(f"  - Group ID: {group_id}, Group Name: {group_name}")
        print()

get_security_groups_for_network_interfaces()
