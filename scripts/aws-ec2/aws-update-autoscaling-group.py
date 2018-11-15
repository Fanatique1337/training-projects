#!/usr/bin/env python3

# DEFAULT IMPORTS:

import argparse
import configparser
import datetime
import json
import os
import subprocess
import sys
from collections import OrderedDict, namedtuple

# THIRD-PARTY IMPORTS:

import boto3
import botocore.exceptions

# DEFINING CONSTANTS:

DEBUG_TRACE = True
DEFAULT_CREDENTIALS_FILE_PATH = "/home/pavlin/.aws/credentials"

# ERROR EXIT CODES:

ARGPARSE_ERR    = 4
BOTO3_API_ERR   = 5
CREDENTIALS_ERR = 6
GLOBAL_ERR      = 9

def get_arguments():

    parser = argparse.ArgumentParser(description="Amazon EC2 Auto Backup")

    parser.add_argument("--credentialsfile",
                        help="Select a custom credentials file.",
                        type=str)
    parser.add_argument("--region",
                        help="Choose an AWS region.",
                        type=str)

    return parser.parse_args()

def get_credentials(credentials_file_path=DEFAULT_CREDENTIALS_FILE_PATH):

    credentials_config = configparser.ConfigParser()
    credentials_config.read(credentials_file_path)

    secret_key = credentials_config['default']['aws_secret_access_key']
    key_id     = credentials_config['default']['aws_access_key_id']
        
    credentials_tup = namedtuple("Credentials", "secret_key key_id")
    credentials     = credentials_tup(secret_key=secret_key, key_id=key_id)

    return credentials

def init_client(service, credentials, region=None):

    session = boto3.session.Session(
        aws_access_key_id     = credentials.key_id,
        aws_secret_access_key = credentials.secret_key,
        region_name           = region)

    return session.client(
        service_name          = service,
        region_name           = region,
        aws_access_key_id     = credentials.key_id,
        aws_secret_access_key = credentials.secret_key
    )

def get_instances(client):
    instance_map = {}
    instance_ids = []

    describe_instances = client.describe_instances()

    for reservation in describe_instances["Reservations"]:
        for instance in reservation["Instances"]:
            instance_ids.append(instance["InstanceId"])
            for tag in instance["Tags"]:
                if tag["Key"] == "Name":
                    instance_map[tag["Value"]] = instance["InstanceId"]

    return instance_map, instance_ids

def backup_image(client, instance):

    image_response  = client.create_image(
        Description = "Automated backup image",
        NoReboot    = True,
        InstanceId  = instance,
        DryRun      = False,
        Name        = "Automated image {}".format(get_current_date())
    )

    return image_response["ImageId"]

def get_current_date():

    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

def get_launch_configuration(client, name=None):
    launch_configurations = client.describe_launch_configurations()

    if name:
        for config in launch_configurations["LaunchConfigurations"]:
            if config["LaunchConfigurationName"] == name:
                launch_configuration = config
    else:
        launch_configuration = launch_configurations["LaunchConfigurations"][0]

    return launch_configuration

def update_launch_configuration(client, launch_configuration, image):

    launch_configuration["ImageId"] = image
    for_deletion_name = launch_configuration["LaunchConfigurationName"]
    launch_configuration["LaunchConfigurationName"] = "LaunchConfig {}".format(
        get_current_date())

    new_configuration = build_launch_configuration(launch_configuration)

    creation_response = client.create_launch_configuration(**new_configuration)

    return creation_response


def build_launch_configuration(data):

    configuration = OrderedDict(
        LaunchConfigurationName      = data["LaunchConfigurationName"],
        ImageId                      = data["ImageId"],
        KeyName                      = data["KeyName"],
        SecurityGroups               = data["SecurityGroups"],
        ClassicLinkVPCSecurityGroups = data["ClassicLinkVPCSecurityGroups"],
        InstanceType                 = data["InstanceType"],
        BlockDeviceMappings          = data["BlockDeviceMappings"],
        InstanceMonitoring           = data["InstanceMonitoring"],
        )

    return configuration

def update_auto_scaling_group(client, group_name, launch_config_name):
    
    return client.update_auto_scaling_group(
        AutoScalingGroupName    = group_name,
        LaunchConfigurationName = launch_config_name
    )

def main():

    credentials = get_credentials('/home/pavlin/.aws/credentials')

    print(credentials.key_id)

    ec2_client = init_client(
        service     = "ec2", 
        credentials = credentials, 
        region      = "eu-central-1"
    )

    autoscaling_client = init_client(
        service     = "autoscaling",
        credentials = credentials,
        region      = "eu-central-1"
    )

    instance_map, instance_ids = get_instances(ec2_client)
    image_id = backup_image(ec2_client, instance_map["instance_1"])
    print(image_id)
    launch_configuration = get_launch_configuration(autoscaling_client)
    launch_configuration_name = launch_configuration["LaunchConfigurationName"]

    creation = update_launch_configuration(
        client = autoscaling_client, 
        launch_configuration = launch_configuration, 
        image = image_id
    )

    print(instance_map)
    print(instance_ids)

    print(creation)

    autoscaling_update = update_auto_scaling_group(
        client             = autoscaling_client,
        launch_config_name = launch_configuration["LaunchConfigurationName"],
        group_name         = "AutoScalingGroup1"
    )

    deletion_response = ec2_client.delete_launch_configuration(
        LaunchConfigurationName=launch_configuration_name)

    print(autoscaling_update)
    print(deletion_response)

main()