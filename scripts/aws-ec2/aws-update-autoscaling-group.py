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

DEBUG_TRACE                   = True
DEFAULT_CREDENTIALS_FILE_PATH = "/home/pavlin/.aws/credentials"
DEFAULT_REGION                = "eu-central-1"

# ERROR EXIT CODES:

ARGPARSE_ERR    = 4
BOTO3_API_ERR   = 5
CREDENTIALS_ERR = 6
GLOBAL_ERR      = 9

def get_arguments():

    parser = argparse.ArgumentParser(description="Amazon EC2 Auto Backup")

    parser.add_argument("--credentialsfile",
                        help="Select a custom credentials file.",
                        type=str,
                        default=DEFAULT_CREDENTIALS_FILE_PATH)
    parser.add_argument("--region",
                        help="Choose an AWS region.",
                        type=str,
                        default=DEFAULT_REGION)

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
    instance_ids = []
    allowed_states = ["running"]
    filters_dict = OrderedDict(
        Name   = "instance-state-name",
        Values = allowed_states
    )

    describe_instances = client.describe_instances(
        Filters = [filters_dict]
    )

    for reservation in describe_instances["Reservations"]:
        for instance in reservation["Instances"]:
            instance_ids.append(instance["InstanceId"])

    return instance_ids

def backup_image(client, instance):

    image_response  = client.create_image(
        Description = "Automated backup image",
        NoReboot    = True,
        InstanceId  = instance,
        DryRun      = False,
        Name        = "ami-{}-{}".format(instance, get_current_date())
    )

    return image_response["ImageId"]

def get_current_date():

    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

def get_launch_configuration(client, instance):
    launch_configurations = client.describe_launch_configurations()

    for config in launch_configurations["LaunchConfigurations"]:
        if instance in config["LaunchConfigurationName"]:
            launch_configuration = config
            image_to_delete      = config["ImageId"]

    return launch_configuration, image_to_delete

def update_launch_configuration(client, launch_configuration, image, instance):

    launch_configuration["ImageId"] = image
    launch_configuration["LaunchConfigurationName"] = "lc-{}-{}".format(
        instance, get_current_date())

    new_configuration = build_launch_configuration(launch_configuration)

    client.create_launch_configuration(**new_configuration)

    return new_configuration

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

def delete_image(client, image):

    image_snapshots = []

    image_data = client.describe_images(
        ImageIds  = [image],
        DryRun    = False
    )

    for device in image_data["Images"][0]["BlockDeviceMappings"]:
        image_snapshots.append(device["Ebs"]["SnapshotId"])

    deregister_response = client.deregister_image(
        ImageId = image,
        DryRun  = False
    )

    print("Deregistered image: '{}'".format(image))

    for snapshot in image_snapshots:
        snapshot_response = client.delete_snapshot(
            SnapshotId = snapshot,
            DryRun     = False
        )

        print("Deleted snapshot: '{}'".format(snapshot))

def main():

    args = get_arguments()

    credentials = get_credentials(args.credentialsfile)

    ec2_client = init_client(
        service     = "ec2", 
        credentials = credentials, 
        region      = args.region
    )

    autoscaling_client = init_client(
        service     = "autoscaling",
        credentials = credentials,
        region      = args.region
    )

    instance_ids = get_instances(ec2_client)
    instance_map = {}

    for instance in instance_ids:
        print("Started backing up instance {}".format(instance))
        image_id = backup_image(ec2_client, instance)
        print("Created image: '{}'".format(image_id))

        instance_map[image_id] = instance

        launch_configuration, image_to_delete = get_launch_configuration(
            client   = autoscaling_client,
            instance = instance
        )

        old_launch_config = launch_configuration["LaunchConfigurationName"]

        new_launch_config = update_launch_configuration(
            client               = autoscaling_client,
            launch_configuration = launch_configuration,
            image                = image_id,
            instance             = instance
        )
        print("Created new launch configuration: '{}'".format(
            new_launch_config["LaunchConfigurationName"])
        )

        autoscaling_update = update_auto_scaling_group(
            client             = autoscaling_client,
            launch_config_name = new_launch_config["LaunchConfigurationName"],
            group_name         = "ac-{}".format(instance)
        )
        print("Updated autoscaling group: 'ac-{}'".format(instance))

        autoscaling_client.delete_launch_configuration(
            LaunchConfigurationName=old_launch_config
        )
        print("Deleted launch configuration: '{}'".format(old_launch_config))

        delete_image(ec2_client, image_to_delete)
        print("Deleted image: '{}'".format(image_to_delete))

main()
