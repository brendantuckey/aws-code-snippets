"""
Modify a security group using Client.authorize_security_group_ingress and Resource.revoke_ingress

Technologies: python, boto3

Documentation
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/authorize_security_group_ingress.html
    https://boto3.amazonaws.com/v1/documentation/api/1.26.92/reference/services/ec2/securitygroup/revoke_ingress.html

Run in Cloud 9:
    python3 boto3-create-security-group.py
OR
    Run button from code editor

Author: Brendan Tuckey
Repo location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/25/2024
"""

#!/usr/bin/python3
import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')

groupid = 'sg-07f99a7c527820059'

#-----------------------------------------------------
# Modify the security group to add the 2222 port (Same as to create)
#-----------------------------------------------------
response = ec2.authorize_security_group_ingress(GroupId=groupid,
                                                IpPermissions=[
                                                    {'FromPort': 2222,
                                                     'IpProtocol': 'tcp',
                                                     'IpRanges': [
                                                         {'CidrIp': '1.1.1.1/32',
                                                          'Description': 'Port 2222 access from the my virtual office',
                                                          },],
                                                     'ToPort': 2222,},
                                                     ])
print(response)

#-----------------------------------------------------
# What if I wanted to remove an ingress
#-----------------------------------------------------

# resource.revoke_ingress function removes a security group ingress
# or client.revoke_security_group_ingress

ec2 = boto3.resource('ec2')

security_group = ec2.SecurityGroup('sg-07f99a7c527820059')
for rule in security_group.ip_permissions:
    if rule['IpProtocol'] == 'tcp' and rule['FromPort'] == 80 and rule['ToPort'] == 80:
        for ip_range in rule['IpRanges']:
            if ip_range['CidrIp'] == '0.0.0.0/0':
                print("Found rule and will now revoke...")
                security_group.revoke_ingress(
                    IpProtocol='tcp',
                    FromPort=80,
                    ToPort=80,
                    CidrIp='0.0.0.0/0'
                )
