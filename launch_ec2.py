#!/usr/bin/env python3
"""
AWS LAB01 - EC2 Instance Launch Automation

This script demonstrates how to use boto3 to launch an EC2 instance in AWS.
It covers basic EC2 instance creation with tags and waiting for the instance to be running.

"""

import boto3
import time
from botocore.exceptions import ClientError



# Initialize the EC2 client
ec2_client = boto3.client("ec2","eu-north-1")

AMI_ID = 'ami-0f670ce69a22c07a9'  # Amazon Linux 2023 AMI in eu-north-1
INSTANCE_TYPE = 't3.micro'
KEY_NAME = 'keyconnect'  # Replace with your key pair name
SECURITY_GROUP_ID = 'sg-08c4132223d3f1951'  # Replace with your security group ID
SUBNET_ID = "subnet-0a5add626bba508cd"  # Replace with your subnet ID

INSTANCE_TAGS = [
    {
        'Key': 'Name',
        'Value': 'philip-boto3'
    },
    {
        'Key': 'Environment',
        'Value': 'Training'
    },
    {
        'Key': 'Project',
        'Value': 'philip-labs'
    }
]



def launch_instance():
    """Launch an EC2 instance with the specified configuration."""
    try:
        response = ec2_client.run_instances(
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE,
            KeyName=KEY_NAME,
            SecurityGroupIds=[SECURITY_GROUP_ID],
            MinCount=1,
            MaxCount=1,
            SubnetId="subnet-0a5add626bba508cd",
            TagSpecifications=[

                {
                    'ResourceType': 'instance',
                    'Tags': INSTANCE_TAGS
                }
            ]

        )


        
        instance_id = response["Instances"][0]["InstanceId"]
        print(f"Launched EC2 instance: {instance_id}")
        
        return instance_id
    except ClientError as e:
        print(f"Error launching EC2 instance: {e}")
        return None
    
    

def wait_for_instance(instance_id):
    """ Wait for the instance to be in a running state """
    try:
        print("Waiting for instance to start running...")
        
        instance = None
        instance_state = None
        counter = 0

        while instance_state != 'running' and counter < 24:

            response = ec2_client.describe_instances(InstanceIds=[instance_id])
            instance = response['Reservations'][0]['Instances'][0]
            instance_state = instance['State']['Name']

            if instance_state == 'running':
                break

            counter += 1

            time.sleep(5)

        if instance_state != 'running':
            raise Exception("Instance did not start")

        return instance      

    except ClientError as e:
        print(f"Error waiting for instance: {e}")
        return None



def display_instance_details(instance):
    """Display relevant details of the EC2 instance."""

    print(f"instance ID: {instance['InstanceId']}")
    print(f"instance state: {instance['State']['Name']}")
    print(f"instance type: {instance['InstanceType']}")
    print(f"Image ID: {instance['ImageId']}")
    print(f"public DNS: {instance['PublicDnsName']}")
    print(f"public IP Address: {instance['PublicIpAddress']}")
    print(f"Private IP Address: {instance['PrivateIpAddress']}")
    print(f"Tags: {instance['Tags']}")



def terminate_instance(instance_id):
    """Terminate the EC2 instance."""
    try:
        print(f"\nTerminating instance: {instance_id}")
        ec2_client.terminate_instances(InstanceIds=[instance_id])

        print(f"waiting for instance to terminate...")

        instance = None
        instance_state = None
        counter = 0

        while instance_state != 'terminated' and counter < 48:
            response = ec2_client.describe_instances(InstanceIds=[instance_id])
            instance = response['Reservations'][0]['Instances'][0]
            instance_state = instance['State']['Name']

            if instance_state == 'terminated':
                break

            counter += 1

            time.sleep(10)

        if instance_state != 'terminated':
            raise Exception("Failed to terminate instance")
        return instance_state == "terminated"
            
    except ClientError as e:
        print(f"Error terminating instance: {e}")
        return False
    
    

if __name__ == "__main__":
    print("AWS EC2 Instance Launch Tool")
    print("===========================")
    
    instance_id = launch_instance()
    if not instance_id:
        exit(1)
        
    instance = wait_for_instance(instance_id)
    if not instance:
            exit(1)
            
    display_instance_details(instance)
    
    print(f"\nSSH Command:")
    print(f"ssh -i your-ssh-file.pem ec2-user@{instance['PublicDnsName']}")
    
    print("\n⚠️  IMPORTANT: Remember to terminate this instance when done to avoid charges!")
    
    
    # Uncomment below line to automatically terminate the instance after inspection
    # terminate_instance(instance_id)