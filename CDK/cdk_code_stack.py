"""
Objective: Build an Application Load Balancer, Listener and Auto
Scaling Group on AWS Cloud9 with AWS Cloud Development Kit using Python.

Technologies: python, aws_cdk, Cloud9

Related Documentation:

Accompanying files:
    httpd-install.sh    --> Used for the user data script for the EC2 Instance

To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/CDK
Updated: 3/29/2024
"""

from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    App, CfnOutput, Stack
)
from constructs import Construct

class CdkCodeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "VPC")
        data = open("./httpd-install.sh", "rb").read()
        httpd=ec2.UserData.for_linux()
        httpd.add_commands(str(data,'utf-8'))
        asg = autoscaling.AutoScalingGroup(
            self,
            "ASG",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            user_data=httpd
        )
        
        lb = elbv2.ApplicationLoadBalancer(
            self,
            "LB",
            vpc=vpc,
            internet_facing=True
        )
            
        listener = lb.add_listener("Listener", port=80)
        listener.add_targets("Target", port=80, targets=[asg])
        listener.connections.allow_default_port_from_any_ipv4("Open to the world")
        
        asg.scale_on_request_count("AModestLoad", target_requests_per_minute=60)
        CfnOutput(self,"Winter2024",export_name="Winter2024",value=lb.load_balancer_dns_name)