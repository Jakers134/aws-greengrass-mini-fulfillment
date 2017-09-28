#!/usr/bin/env python

# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License is
# located at
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

import fire
import json
import logging

from gg_group_setup import GroupConfigFile
from gg_group_setup import GroupCommands
from gg_group_setup import GroupType


logging.basicConfig(format='%(asctime)s|%(name)-8s|%(levelname)s: %(message)s',
                    level=logging.INFO)


class MasterGroupType(GroupType):
    """
    Sub-class containing the definitions and subscriptions for the Master Group.
    """
    MASTER_TYPE = 'master'

    def __init__(self, config=None, region='us-west-2'):
        super(MasterGroupType, self).__init__(
            type_name=MasterGroupType.MASTER_TYPE, config=config, region=region
        )

    def get_core_definition(self, config):
        """
        Get the Master Group Type's core definition

        :param config: gg_group_setup.GroupConfigFile used with the Group Type
        :return: the core definition used to provision the group
        """
        cfg = config
        definition = [{
            "ThingArn": cfg['core']['thing_arn'],
            "CertificateArn": cfg['core']['cert_arn'],
            "Id": "{0}_00".format(self.type_name),  # arbitrary unique Id string
            "SyncShadow": True
        }]
        logging.debug('[master.get_core_definition] definition:{0}'.format(
            definition)
        )
        return definition

    def get_device_definition(self, config):
        """
        Get the Master Group Type's device definition

        :param config: gg_group_setup.GroupConfigFile used with the Group Type
        :return: the device definition used to provision the group
        """
        cfg = config
        definition = [
            {
                "Id": "{0}_10".format(self.type_name),
                "ThingArn": cfg['devices']['GGD_belt']['thing_arn'],
                "CertificateArn": cfg['devices']['GGD_belt'][
                    'cert_arn'],
                "SyncShadow": False
            },
            {
                "Id": "{0}_11".format(self.type_name),
                "ThingArn": cfg['devices']['GGD_bridge']['thing_arn'],
                "CertificateArn": cfg['devices']['GGD_bridge'][
                    'cert_arn'],
                "SyncShadow": False
            },
            {
                "Id": "{0}_12".format(self.type_name),
                "ThingArn": cfg['devices']['GGD_button']['thing_arn'],
                "CertificateArn": cfg['devices']['GGD_button'][
                    'cert_arn'],
                "SyncShadow": False
            },
            {
                "Id": "{0}_13".format(self.type_name),
                "ThingArn": cfg['devices']['GGD_inv_arm']['thing_arn'],
                "CertificateArn": cfg['devices']['GGD_inv_arm'][
                    'cert_arn'],
                "SyncShadow": False
            },
            {
                "Id": "{0}_14".format(self.type_name),
                "ThingArn": cfg['devices']['GGD_sort_arm']['thing_arn'],
                "CertificateArn": cfg['devices']['GGD_sort_arm'][
                    'cert_arn'],
                "SyncShadow": False
            },
            {
                "Id": "{0}_15".format(self.type_name),
                "ThingArn": cfg['devices']['GGD_heartbeat'][
                    'thing_arn'],
                "CertificateArn": cfg['devices']['GGD_heartbeat'][
                    'cert_arn'],
                "SyncShadow": False
            },
            {
                "Id": "{0}_16".format(self.type_name),
                "ThingArn": cfg['devices']['GGD_web']['thing_arn'],
                "CertificateArn": cfg['devices']['GGD_web']['cert_arn'],
                "SyncShadow": False
            }
        ]
        logging.debug('[master.get_device_definition] definition:{0}'.format(
            definition)
        )
        return definition

    def get_subscription_definition(self, config):
        """
        Get the Master Group Type's subscription definition

        :param config: gg_group_setup.GroupConfigFile used with the Group Type
        :return: the subscription definition used to provision the group
        """
        cfg = config
        d = cfg['devices']
        l = cfg['lambda_functions']
        s = cfg['subscriptions']

        definition = [
            {  # from Master belt device to MasterErrorDetector Lambda
                "Id": "5",
                "Source": d['GGD_belt']['thing_arn'],
                "Subject": s['telemetry'],
                "Target": l['MasterErrorDetector']['arn']
            },
            {  # from Master belt device to web device
                "Id": "10",
                "Source": d['GGD_belt']['thing_arn'],
                "Subject": s['all'],
                "Target": d['GGD_web']['thing_arn']
            },
            {  # from Master belt device to MasterBrain Lambda
                "Id": "11",
                "Source": d['GGD_belt']['thing_arn'],
                "Subject": s['stages'],
                "Target": l['MasterBrain']['arn']
            },
            {  # from MasterErrorDetector to MasterBrain Lambda
                "Id": "12",
                "Source": l['MasterErrorDetector']['arn'],
                "Subject": s['errors'],
                "Target": l['MasterBrain']['arn']
            },
            {  # from MasterErrorDetector to AWS cloud
                "Id": "13",
                "Source": l['MasterErrorDetector']['arn'],
                "Subject": s['errors'],
                "Target": "cloud"
            },
            {  # from Master belt device to AWS cloud
                "Id": "15",
                "Source": d['GGD_belt']['thing_arn'],
                "Subject": s['stages'],
                "Target": "cloud"
            },
            {  # from Master web device to Greengrass Core local shadow
                "Id": "16",
                "Source": d['GGD_web']['thing_arn'],
                "Subject": "$aws/things/MasterBrain/shadow/get",
                "Target": "GGShadowService"
            },
            {  # from Greengrass Core local shadow to Master web device
                "Id": "17",
                "Source": "GGShadowService",
                "Subject": "$aws/things/MasterBrain/shadow/get/#",
                "Target": d['GGD_web']['thing_arn']
            },
            {  # from Master bridge device to Master web device
                "Id": "18",
                "Source": d['GGD_bridge']['thing_arn'],
                "Subject": "/sort/arm/#",
                "Target": d['GGD_web']['thing_arn']
            },
            {  # from Master bridge device to MasterBrain Lambda
                "Id": "19",
                "Source": d['GGD_bridge']['thing_arn'],
                "Subject": "/sort/arm/stages",
                "Target": l['MasterBrain']['arn']
            },
            {  # from Master bridge device to MasterBrain Lambda
                "Id": "20",
                "Source": d['GGD_bridge']['thing_arn'],
                "Subject": "/sort/arm/errors",
                "Target": l['MasterBrain']['arn']
            },
            {  # from Master bridge device to MasterBrain Lambda, stages topic
                "Id": "21",
                "Source": d['GGD_bridge']['thing_arn'],
                "Subject": "/inv/arm/stages",
                "Target": l['MasterBrain']['arn']
            },
            {  # from Master bridge device to MasterBrain Lambda, errors topic
                "Id": "22",
                "Source": d['GGD_bridge']['thing_arn'],
                "Subject": "/inv/arm/errors",
                "Target": l['MasterBrain']['arn']
            },
            {  # from Master bridge device to Master web device, all topics
                "Id": "23",
                "Source": d['GGD_bridge']['thing_arn'],
                "Subject": "/inv/arm/#",
                "Target": d['GGD_web']['thing_arn']
            },
            {  # from Master belt device to Greengrass Core local shadow, get
                "Id": "31",
                "Source": d['GGD_belt']['thing_arn'],
                "Subject": "$aws/things/MasterBrain/shadow/get",
                "Target": "GGShadowService"
            },
            {  # from Greengrass Core local shadow to Master belt device, get
                "Id": "32",
                "Source": "GGShadowService",
                "Subject": "$aws/things/MasterBrain/shadow/get/#",
                "Target": d['GGD_belt']['thing_arn']
            },
            {  # from Master belt device to Greengrass Core local shadow, update
                "Id": "34",
                "Source": d['GGD_belt']['thing_arn'],
                "Subject": "$aws/things/MasterBrain/shadow/update",
                "Target": "GGShadowService"
            },
            {  # from Greengrass Core local shadow to Master belt device, update
                "Id": "35",
                "Source": "GGShadowService",
                "Subject": "$aws/things/MasterBrain/shadow/update/#",
                "Target": d['GGD_belt']['thing_arn']
            },
            {  # from InvArm arm device to Master Greengrass Core local shadow
                "Id": "84",
                "Source": d['GGD_inv_arm']['thing_arn'],  # GGD matches ArmType
                "Subject": "$aws/things/MasterBrain/shadow/get",
                "Target": "GGShadowService"
            },
            {  # from Master Greengrass Core local shadow to InvArm arm device
                "Id": "85",
                "Source": "GGShadowService",
                "Subject": "$aws/things/MasterBrain/shadow/get/#",
                "Target": d['GGD_inv_arm']['thing_arn']  # GGD matches ArmType
            },
            {  # from InvArm arm device to Master Greengrass Core local shadow
                "Id": "86",
                "Source": d['GGD_inv_arm']['thing_arn'],  # GGD matches ArmType
                "Subject": "$aws/things/MasterBrain/shadow/update",
                "Target": "GGShadowService"
            },
            {  # from Master Greengrass Core local shadow to InvArm arm device
                "Id": "87",
                "Source": "GGShadowService",
                "Subject": "$aws/things/MasterBrain/shadow/update/#",
                "Target": d['GGD_inv_arm']['thing_arn']  # GGD matches ArmType
            },
            {  # from SortArm arm device to Master Greengrass Core local shadow
                "Id": "92",
                "Source": d['GGD_sort_arm']['thing_arn'],  # GGD matches ArmType
                "Subject": "$aws/things/MasterBrain/shadow/get",
                "Target": "GGShadowService"
            },
            {  # from Master Greengrass Core local shadow to SortArm arm device
                "Id": "93",
                "Source": "GGShadowService",
                "Subject": "$aws/things/MasterBrain/shadow/get/#",
                "Target": d['GGD_sort_arm']['thing_arn']  # GGD matches ArmType
            },
            {  # from SortArm arm device to Master Greengrass Core local shadow
                "Id": "94",
                "Source": d['GGD_sort_arm']['thing_arn'],  # GGD matches ArmType
                "Subject": "$aws/things/MasterBrain/shadow/update",
                "Target": "GGShadowService"
            },
            {  # from Master Greengrass Core local shadow to SortArm arm device
                "Id": "95",
                "Source": "GGShadowService",
                "Subject": "$aws/things/MasterBrain/shadow/update/#",
                "Target": d['GGD_sort_arm']['thing_arn']  # GGD matches ArmType
            },
            {  # from Master heartbeat device to AWS cloud
                "Id": "97",
                "Source": d['GGD_heartbeat']['thing_arn'],
                "Subject": "/heart/beat",
                "Target": "cloud"
            },
            {  # from Master button device to MasterBrain Lambda
                "Id": "98",
                "Source": d['GGD_button']['thing_arn'],
                "Subject": "/button",
                "Target": l['MasterBrain']['arn']
            }
        ]
        logging.debug(
            '[master.get_subscription_definition] definition:{0}'.format(
                definition)
        )
        return definition


class ArmGroupType(GroupType):
    ARM_TYPE = 'arm'

    def __init__(self, config=None, region='us-west-2'):
        super(ArmGroupType, self).__init__(
            type_name=ArmGroupType.ARM_TYPE, config=config, region=region
        )
        self.arm_ggd_name = 'GGD_arm'

    def get_core_definition(self, config):
        """
        Get the Arm Group Type's core definition

        :param config: gg_group_setup.GroupConfigFile used with the Group Type
        :return: the core definition used to provision the group
        """
        cfg = config
        definition = [{
            "ThingArn": cfg['core']['thing_arn'],
            "CertificateArn": cfg['core']['cert_arn'],
            "Id": "{0}_00".format(self.type_name),
            "SyncShadow": True
        }]
        logging.debug(
            '[arm.get_core_definition] definition:{0}'.format(
                definition)
        )
        return definition

    def get_device_definition(self, config):
        """
        Get the Arm Group Type's device definition

        :param config: gg_group_setup.GroupConfigFile used with the Group Type
        :return: the device definition used to provision the group
        """
        cfg = config
        definition = [
            {
                "Id": "{0}_20".format(self.type_name),
                "ThingArn": cfg['devices'][self.arm_ggd_name]['thing_arn'],
                "CertificateArn": cfg['devices'][self.arm_ggd_name]['cert_arn'],
                "SyncShadow": False
            },
            {
                "Id": "{0}_21".format(self.type_name),
                "ThingArn": cfg['devices']['GGD_bridge']['thing_arn'],
                "CertificateArn": cfg['devices']['GGD_bridge']['cert_arn'],
                "SyncShadow": False
            },
            {
                "Id": "{0}_22".format(self.type_name),
                "ThingArn": cfg['devices']['GGD_heartbeat']['thing_arn'],
                "CertificateArn": cfg['devices']['GGD_heartbeat']['cert_arn'],
                "SyncShadow": False
            }
        ]
        logging.debug(
            '[arm.get_device_definition] definition:{0}'.format(
                definition)
        )

        return definition

    def get_subscription_definition(self, config):
        """
        Get the Arm Group Type's subscription definition

        :param config: gg_group_setup.GroupConfigFile used with the Group Type
        :return: the subscription definition used to provision the group
        """
        cfg = config
        d = cfg['devices']
        l = cfg['lambda_functions']
        s = cfg['subscriptions']

        definition = [
            {  # from Group's arm device to bridge device
                "Id": "40",
                "Source": d[self.arm_ggd_name]['thing_arn'],
                "Subject": s["all"],
                "Target": d['GGD_bridge']['thing_arn']
            },
            {  # from Group's arm device to AWS cloud
                "Id": "41",
                "Source": d[self.arm_ggd_name]['thing_arn'],
                "Subject": s['stages'],
                "Target": "cloud"
            },
            {  # from Group's arm device ArmErrorDetector Lambda
                "Id": "42",
                "Source": d[self.arm_ggd_name]['thing_arn'],
                "Subject": s['telemetry'],
                "Target": l['ArmErrorDetector']['arn']
            },
            {  # from ArmErrorDetector Lambda to bridge device
                "Id": "50",
                "Source": l['ArmErrorDetector']['arn'],
                "Subject": s['errors'],
                "Target": d['GGD_bridge']['thing_arn']
            },
            {  # from ArmErrorDetector Lambda to AWS cloud
                "Id": "51",
                "Source": l['ArmErrorDetector']['arn'],
                "Subject": s['errors'],
                "Target": "cloud"
            },
            {  # from Group's heartbeat device to bridge device
                "Id": "95",
                "Source": d['GGD_heartbeat']['thing_arn'],
                "Subject": "/heart/beat",
                "Target": d['GGD_bridge']['thing_arn']
            },
            {  # from Group's heartbeat device to AWS cloud
                "Id": "97",
                "Source": d['GGD_heartbeat']['thing_arn'],
                "Subject": "/heart/beat",
                "Target": "cloud"
            }
        ]
        logging.debug(
            '[arm.get_subscription_definition] definition:{0}'.format(
                definition)
        )

        return definition


class SortArmGroupType(ArmGroupType):
    ARM_TYPE = 'sort_arm'

    def __init__(self, config=None, region='us-west-2'):
        super(ArmGroupType, self).__init__(
            type_name=ArmGroupType.ARM_TYPE, config=config, region=region
        )
        self.arm_ggd_name = 'GGD_sort_arm'


class InvArmGroupType(ArmGroupType):
    ARM_TYPE = 'inv_arm'

    def __init__(self, config=None, region='us-west-2'):
        super(ArmGroupType, self).__init__(
            type_name=ArmGroupType.ARM_TYPE, config=config, region=region
        )
        self.arm_ggd_name = 'GGD_inv_arm'


class MiniFulfillmentGroupCommands(GroupCommands):

    def __init__(self):
        super(MiniFulfillmentGroupCommands, self).__init__(group_types={
            MasterGroupType.MASTER_TYPE: MasterGroupType,
            SortArmGroupType.ARM_TYPE: SortArmGroupType,
            InvArmGroupType.ARM_TYPE: InvArmGroupType
        })

    @staticmethod
    def associate_lambda(group_config, lambda_config):
        """
        Associate the Lambda described in the `lambda_config` with the
        Greengrass Group described by the `group_config`

        :param group_config: `gg_group_setup.GroupConfigFile` to store the group
        :param lambda_config: the configuration describing the Lambda to
            associate with the Greengrass Group

        :return:
        """
        with open(lambda_config, "r") as f:
            cfg = json.load(f)

        config = GroupConfigFile(config_file=group_config)

        lambdas = config['lambda_functions']
        lambdas[cfg['func_name']] = {
            'arn': cfg['lambda_arn'],
            'arn_qualifier': cfg['lambda_alias']
        }

        config['lambda_functions'] = lambdas


if __name__ == '__main__':
    """
    Instantiate a subclass of the `gg_group_setup.GroupCommands` object that 
    uses the two sub-classed GroupType classes. 
    
    The sub-class of GroupCommands will then use the sub-classed GroupTypes to 
    expose the `create`, `deploy`, `clean-all`, `clean-file`, etc. commands.
    
    Note: executing `clean-file` will result in stranded provisioned artifacts 
    in the AWS Greengrass service. These will artifacts will need manual 
    removal.
    """
    fire.Fire(MiniFulfillmentGroupCommands())
