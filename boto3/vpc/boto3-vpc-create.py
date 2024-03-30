"""
Creates a simple VPC with 2 public and 2 private subnets

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

#!/usr/bin/python3
import boto3
from botocore.exceptions import ClientError

VPC_Name = "My_Test_VPC"
REGION = 'us-east-1'
ec2 = boto3.resource('ec2', region_name=REGION)

#---------------------------------------------------------------
# Create the VPC
#---------------------------------------------------------------
vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')

# we can assign a name to vpc, or any resource, by using tag
vpc.create_tags(Tags=[{"Key": "Name", "Value": VPC_Name}])
vpc.wait_until_available()
print(vpc.id)

#---------------------------------------------------------------
# Public Route table and 2 subnets (with Internet gateway)
#---------------------------------------------------------------

#---------------------------------------------------------------
# create then attach internet gateway (IG)
#---------------------------------------------------------------
ig = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=ig.id)
print(ig.id)

# create a default route table and a public route to use our IG
public_route_table = vpc.create_route_table()
route = public_route_table.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=ig.id) # this makes it public
print(public_route_table.id)

# create subnet
try: 
    subnet1 = ec2.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc.id, AvailabilityZone=REGION+'a')
    print(subnet1.id)
    # create subnet
    subnet2 = ec2.create_subnet(CidrBlock='192.168.2.0/24', VpcId=vpc.id, AvailabilityZone=REGION+'b')
    print(subnet2.id)
except Exception as e:
    print("Exception creating the public subnet", e)

# associate the route table with the subnet
try:
    public_route_table.associate_with_subnet(SubnetId=subnet1.id)
    public_route_table.associate_with_subnet(SubnetId=subnet2.id)
except Exception as e:
    print("Exception associateing the public subnet", e)
#---------------------------------------------------------------
# Private Route table and 2 subnets (with NAT gateway)
#---------------------------------------------------------------

ec2_client = boto3.client('ec2')
# Allocate an Elastic IP address for the NAT gateway
response = ec2_client.allocate_address(Domain='vpc')  # Specify 'vpc' to allocate it for use with VPC

# Extract the Elastic IP address ID from the response and add a tag so we can identify it later
eip_allocation_id = response['AllocationId']
tag_name = VPC_Name + "_EIP - release promptly"
ec2_client.create_tags(
    Resources=[eip_allocation_id],
    Tags=[{'Key': 'Name', 'Value': tag_name}]
)

# Create a NAT Gateway
nat_gateway_response = ec2_client.create_nat_gateway(
    SubnetId=subnet1.id,
    AllocationId=eip_allocation_id  # Elastic IP allocation ID we just created
)

# Extract the NAT Gateway ID from the response
nat_gateway_id = nat_gateway_response['NatGateway']['NatGatewayId']
print("Waiting for the NAT Gateway to become available. This takes a little while...")

# Wait for the NAT Gateway to be available
ec2_client.get_waiter('nat_gateway_available').wait(NatGatewayIds=[nat_gateway_id])


# create a default route table and a public route to use our NAT Gateway
private_route_table = vpc.create_route_table()

route = private_route_table.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    NatGatewayId=nat_gateway_id) 
print(private_route_table.id)

# create subnet
try:
    subnet3 = ec2.create_subnet(CidrBlock='192.168.3.0/24', VpcId=vpc.id, AvailabilityZone=REGION+'a') 
    print(subnet3.id)
    # create subnet
    subnet4 = ec2.create_subnet(CidrBlock='192.168.4.0/24', VpcId=vpc.id, AvailabilityZone=REGION+'b')
    print(subnet4.id)
except Exception as e:
    print("Exception creating the private subnet", e)

# associate the route table with the subnet
try:
    private_route_table.associate_with_subnet(SubnetId=subnet3.id)
    private_route_table.associate_with_subnet(SubnetId=subnet4.id)
except Exception as e:
    print("Exception associateing the private subnet", e)

"""
To Remove the VPC etc created in this file:
    Delete the NAT Gateway
    Delete the VPC
    Release the Elastic IP

"""