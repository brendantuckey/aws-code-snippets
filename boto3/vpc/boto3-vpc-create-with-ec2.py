"""
Creates a simple VPC with 1 public subnet and launches an EC2 Instance in it
which allows ssh (port 22) access from your current IP

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/index.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_vpc.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_internet_gateway.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_route_table.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_nat_gateway.html

To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/vpc
Updated: 3/29/2024

"""

import boto3
from requests import get

"""
Creates an EC2 instance in a VPC
"""
TAG = 'quick-ec2'
CIDR = '192.168.1.0/24'
client = boto3.client('ec2', 'us-east-1')
resource = boto3.resource('ec2', 'us-east-1')

#Create the VPC
vpcInit = client.create_vpc(CidrBlock=CIDR)
#Get the VPC Id
vpc = resource.Vpc(vpcInit["Vpc"]["VpcId"])
#Add some tags to the VPC 
vpc.create_tags(Tags=[{"Key": "Name", "Value": TAG + "-vpc"}])

# Creating an Internet gateway
igInit = client.create_internet_gateway(TagSpecifications=[
    {'ResourceType': 'internet-gateway',
     'Tags': [{"Key": "Name", "Value": TAG + "-ig"}]
    }
])
igId = igInit["InternetGateway"]["InternetGatewayId"]

#Attaching the IG to our VPC
vpc.attach_internet_gateway(InternetGatewayId=igId)

#Create a route table for our VPC and attach our gateway (making it public)
routeTable = vpc.create_route_table()
route = routeTable.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=igId)
routeTable.create_tags(Tags=[{"Key": "Name", "Value": TAG + "-rt"}])

#Create a subnet and add it to the route table
snName = TAG + '-Subnet'
subnet = vpc.create_subnet(CidrBlock=CIDR,
                           AvailabilityZone="{}{}".format('us-east-1', 'a'))
subnet.create_tags(Tags=[{"Key": "Name", "Value": snName}])

routeTable.associate_with_subnet(SubnetId=subnet.id)

#This gets your home IP address using the 'from requests import get' import above
ip = get('https://api.ipify.org').text
print('Local IP:', ip)

#Set up a security group using your IP
secGroup = resource.create_security_group(GroupName=TAG + '-sg',
                                          Description=TAG + '-SG',
                                          VpcId=vpc.id)
secGroup.authorize_ingress(IpPermissions=[{
    'FromPort': 22,
    'IpProtocol': 'tcp',
    'IpRanges': [{'CidrIp': '{}/32'.format(ip),'Description': 'SSH Access'},],
    'ToPort': 22,
    },
])

#Make a key pair...
#keyFileName = "infraSecrets"
#keyPair = client.create_key_pair(KeyName=keyFileName)
#privateKeyFile = open('{}.pem'.format(keyFileName), "w")
#privateKeyFile.write(dict(keyPair)['KeyMaterial'])
#privateKeyFile.close

#Or just use an existing key pair:
keyFileName = 'brendan-tuckey-internship'

#Finally create the EC2
ec2Instances = resource.create_instances(
    ImageId = 'ami-048f6ed62451373d9',
    InstanceType ='t2.micro', MaxCount = 1, MinCount = 1,
    NetworkInterfaces = [{'SubnetId': subnet.id,'DeviceIndex': 0, 'AssociatePublicIpAddress': True,
                          'Groups': [secGroup.group_id]}],
    KeyName = keyFileName)

instance = ec2Instances[0]
instance.create_tags(Tags=[{"Key": "Name", "Value": TAG}])
print("Waiting for instance to launch. This can take a while...")
instance.wait_until_running()

"""
To completely remove this you need to:
    Terminate the EC2 instance
    Delete the Keypair
    Delete the VPC
"""
