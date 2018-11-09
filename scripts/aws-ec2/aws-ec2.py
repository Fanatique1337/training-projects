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

# DEFINING CONSTANTS:

# ERRORS:

def main():
    instance_ids = []

    client = boto3.client('ec2')

    describe_response = client.describe_instances()

    for reservation in describe_response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_ids.append(instance["InstanceId"])
            print(instance["InstanceId"])

            for tag in instance["Tags"]:
                if tag["Key"] == "Name":
                    print(tag["Value"])

    image_response = client.create_image(
        Description="Automated image",
        NoReboot=True,
        InstanceId=instance_ids[0],
        DryRun=False,
        Name="Automated image 1"
        )

    launch_configuration_data = client.get_launch_template_data(
        InstanceId=instance_ids[0])

    print(image_response)

    print(launch_configuration_data)

    launch_configuration_data["LaunchTemplateData"]["ImageId"] = image_response["ImageId"]

    launch_template_response = client.create_launch_template(
        LaunchTemplateData=launch_configuration_data)
    

main()