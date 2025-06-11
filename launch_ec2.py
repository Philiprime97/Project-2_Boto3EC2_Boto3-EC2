#!/usr/bin/env python3
"""
AWS LAB01 - EC2 Instance Launch Automation

This script demonstrates how to use boto3 to launch an EC2 instance in AWS.
It covers basic EC2 instance creation with tags and waiting for the instance to be running.

Usage:
    python launch_ec2.py
"""

import boto3
import time

from botocore.exceptions import ClientError



# TODO: Initialize the EC2 client with the appropriate region
ec2_client = boto3.client("ec2","eu-north-1")

# Define instance parameters
# TODO: Find and set an appropriate Amazon Linux 2023 AMI ID for eu-east-1
AMI_ID = 'ami-0f670ce69a22c07a9'  # Amazon Linux 2023 AMI in eu-north-1
INSTANCE_TYPE = 't3.micro'
KEY_NAME = 'keyconnect'  # TODO: Set your key pair name
SECURITY_GROUP_ID = 'sg-08c4132223d3f1951'  # TODO: Set your security group ID

# TODO: Define tags to identify your instance
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
    """
    Launch an EC2 instance with defined parameters
    
    Returns:
        str: The ID of the created EC2 instance
    """
    try:
        # TODO: Create a new EC2 instance using run_instances
        # Parameters should include:
        # - ImageId
        # - InstanceType
        # - KeyName
        # - SecurityGroupIds
        # - MinCount/MaxCount
        # - TagSpecifications

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


        
        # TODO: Extract and return the instance ID from the response
        instance_id = response["Instances"][0]["InstanceId"]
        print(f"Launched EC2 instance: {instance_id}")
        
        return instance_id
    except ClientError as e:
        print(f"Error launching EC2 instance: {e}")
        return None

def wait_for_instance(instance_id):
    """
    Wait for the instance to be in a running state
    
    Args:
        instance_id (str): EC2 instance ID
        
    Returns:
        dict: Instance details if successful, None otherwise
    """
    try:
        print("Waiting for instance to start running...")
        
        # TODO: Implement a polling mechanism to check instance state
        # Use describe_instances to get the current state
        # Wait until the state is 'running'
        # Return the instance details once running
        
        # Example structure (you need to complete it):
        # while True:
        #     response = ec2_client.describe_instances(InstanceIds=[instance_id])
        #     instance = response['Reservations'][0]['Instances'][0]
        #     instance_state = instance['State']['Name']
        #     
        #     if instance_state == 'running':
        #         ...

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

        return instance          # TODO: Return the instance details


    except ClientError as e:
        print(f"Error waiting for instance: {e}")
        return None

def display_instance_details(instance):
    """
    Print useful details about the instance
    
    Args:
        instance (dict): EC2 instance details from describe_instances
    """
    # TODO: Print instance details including:
    # - Instance ID
    # - Instance State
    # - Instance Type
    # - AMI ID
    # - Public DNS
    # - Public IP
    # - Private IP
    # - Tags
    
    # Example (you need to complete it):
    # print("\nInstance Details:")
    # print(f"  Instance ID: {instance['InstanceId']}")
    # ...

    print(f"instance ID: {instance['InstanceId']}")
    print(f"instance state: {instance['State']['Name']}")
    print(f"instance type: {instance['InstanceType']}")
    print(f"Image ID: {instance['ImageId']}")
    print(f"public DNS: {instance['PublicDnsName']}")
    print(f"public IP Address: {instance['PublicIpAddress']}")
    print(f"Private IP Address: {instance['PrivateIpAddress']}")
    print(f"Tags: {instance['Tags']}")
    pass

def terminate_instance(instance_id):
    """
    Terminate an EC2 instance
    
    Args:
        instance_id (str): EC2 instance ID
    """
    try:
        # TODO: Implement instance termination
        # Use terminate_instances to terminate the instance
        # Wait for the instance to be terminated
        
        # Example structure (you need to complete it):
        # ec2_client.terminate_instances(InstanceIds=[instance_id])
        # print(f"\nTerminating instance: {instance_id}")
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
    
    # TODO: Launch a new EC2 instance
    instance_id = launch_instance()
    
    # TODO: Wait for the instance to be running
    instance = wait_for_instance(instance_id)


    # TODO: Display instance details
    display_instance_details(instance)
    # TODO: Print SSH connection command if public DNS is available
    print(f"ssh -i your-ssh-file.pem ec2-user@{instance['PublicDnsName']}")
    print("\n⚠️  IMPORTANT: Remember to terminate this instance when done to avoid charges!")
    print("To terminate the instance, implement and call the terminate_instance function.")
    
    # TODO: Uncomment and implement to terminate the instance automatically
    #terminate_instance(instance_id)