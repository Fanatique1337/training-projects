#!/usr/bin/env python3

# DEFAULT IMPORTS:

import argparse
import datetime
import json
import os
import subprocess
import sys
import time
from collections import OrderedDict

# THIRD-PARTY IMPORTS:
 
import boto3 # AWS Python SDK
import botocore.exceptions

# DEFINING CONSTANTS:

# ERRORS:




def clear_dict(config):
    """
    Clear dictionaries from empty values.
    """ 

    return {key: value for key, value in config.items() if value}

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



def main():
    instance_ids = []

    client = boto3.client('ec2')
    autoscaling_client = boto3.client('autoscaling')

    describe_response = client.describe_instances()

    for reservation in describe_response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_ids.append(instance["InstanceId"])
            # print(instance["InstanceId"])

            # for tag in instance["Tags"]:
            #     if tag["Key"] == "Name":
            #         print(tag["Value"])


    image_response = ''
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    try:
        image_response = client.create_image(
            Description="Automated image",
            NoReboot=True,
            InstanceId=instance_ids[0],
            DryRun=False,
            Name="Automated image {}".format(date)
            )
    except botocore.exceptions.ClientError as err:
        print(err)

    #print(image_response) if image_response else print()

    describe_autoscaling_response = autoscaling_client.describe_auto_scaling_groups()
    # print(describe_autoscaling_response)

    launch_configurations = autoscaling_client.describe_launch_configurations()
    print(launch_configurations)
    print()

    for config in launch_configurations["LaunchConfigurations"]:
        if config["LaunchConfigurationName"] == "LaunchConfig1":
            launch_config = config

    launch_config["ImageId"] = image_response["ImageId"]
    launch_config["LaunchConfigurationName"] = "LaunchConfig2"

    new_launch_config = build_launch_configuration(launch_config)
    new_config_response = autoscaling_client.create_launch_configuration(**new_launch_config)
    print(new_config_response)
    print()

    delete_old_config = autoscaling_client.delete_launch_configuration(
        LaunchConfigurationName="LaunchConfig1")

    print(delete_old_config)


main()