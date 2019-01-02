import json

import boto3
from botocore.exceptions import ClientError

from app.read_users_from_file import *
from config import config
from utils.loggingtemplate import logger

try:

    client = boto3.client('iam')

    read_enrolled_users(config.enrolled_users_file)


    def create_iam_group_policy(iam_policy_name, org_path, policy_filename):

        with open(policy_filename) as json_data:
            user_group_permissions_policy = json.load(json_data)
        user_group_permissions_policy_document = json.dumps(user_group_permissions_policy)
        response = client.create_policy(
            PolicyName=iam_policy_name,
            Path=org_path,
            PolicyDocument=user_group_permissions_policy_document,
            Description='Policy gives permission to only Lambda, S3 and API Gateway'
        )
        logger.debug("Success - iam group policy created\n" + str(response))


    def delete_iam_group_policy(policy_arn, org_path, iam_policy_name):

        new_policy_arn = policy_arn + org_path + iam_policy_name
        response = client.delete_policy(
            PolicyArn=new_policy_arn
        )
        logger.debug("Success - Detached the policy from the group\n " + str(response))


    def create_iam_group(org_path, iam_group_name):

        response = client.create_group(
            Path=org_path,
            GroupName=iam_group_name
        )
        logger.debug("Success - iam group created\n" + str(response))


    def delete_iam_group(iam_group_name):

        response = client.delete_group(
            GroupName=iam_group_name
        )
        logger.debug("Success - iam group deleted\n" + str(response))


    def attach_group_policy(policy_arn, org_path, iam_policy_name, iam_group_name):

        new_policy_arn = policy_arn + org_path + iam_policy_name
        response = client.attach_group_policy(
            GroupName=iam_group_name,
            PolicyArn=new_policy_arn
        )
        logger.debug("Success - Attaching the policy to the group\n " + str(response))


    def detach_group_policy(policy_arn, org_path, iam_policy_name, iam_group_name):

        new_policy_arn = policy_arn + org_path + iam_policy_name
        response = client.detach_group_policy(
            GroupName=iam_group_name,
            PolicyArn=new_policy_arn
        )
        logger.debug("Success - Detached the policy to the group\n " + str(response))


    def create_app_specific_role(iam_role_name, org_path, role_policy_filename):

        with open(role_policy_filename) as json_data:
            application_iam_role = json.load(json_data)

        app_role_permissions_policy_document = json.dumps(application_iam_role)

        response = client.create_role(
            Path=org_path,
            RoleName=iam_role_name,
            AssumeRolePolicyDocument=app_role_permissions_policy_document,
            Description='Role created to give sufficient permission for lambda to invoke DynamoDB collections',
            Tags=[
                {
                    'Key': 'app',
                    'Value': 'workshop'
                },
            ]
        )
        logger.debug("Success - Created Application specific role \n" + str(response))


    def delete_app_specific_role(iam_role_name):
        response = client.delete_role(
            RoleName=iam_role_name
        )
        logger.debug("Success - Deleted Application specific role \n" + str(response))


    def create_iam_user(org_path, send_user_name_list):

        logger.debug("Number of users in file - " + str(len(user_name_list)))

        # Delete the below function after debug
        for user_name in user_name_list:
            logger.debug("User name --- " + str(user_name))

        for user_name in user_name_list:
            response = client.create_user(
                Path=org_path,
                UserName=user_name,
                Tags=[
                    {
                        'Key': 'account',
                        'Value': 'workshop'
                    },
                ]
            )
            logger.debug("Success - Created IAM users\n" + str(response))


    def delete_iam_user(user_name_list):

        logger.debug("Number of users in file - " + str(len(user_name_list)))
        for user_name in user_name_list:
            response = client.delete_user(
                UserName=user_name
            )
            logger.debug("Success - Deleted IAM users\n" + str(response))


    def add_user_to_group(iam_group_name, user_name_list):

        for user_name in user_name_list:
            response = client.add_user_to_group(
                GroupName=iam_group_name,
                UserName=user_name
            )
            logger.debug("Success - Added user to the group " + str(response))


    def remove_user_from_group(iam_group_name, user_name_list):

        for user_name in user_name_list:
            response = client.remove_user_from_group(
                GroupName=iam_group_name,
                UserName=user_name
            )
            logger.debug("Success - Removed users from the group " + str(response))


    def create_account_accesskey(user_name_list, first_name_list, last_name_list, email_address_list):

        f = open("accounts-created.txt", "w", encoding='utf-8')

        for i in range(len(user_name_list)):
            response = client.create_access_key(
                UserName=user_name_list[i]
            )
            logger.debug("Success - Created account access key \n" +
                         str(response['AccessKey']['AccessKeyId'] + " --- " +
                             str(response['AccessKey']['SecretAccessKey'])))

            write_to_file = str(response['AccessKey']['AccessKeyId']) + "|#|" + str(
                response['AccessKey']['SecretAccessKey']) + "|#|" + first_name_list[i] + "|#|" + last_name_list[
                                i] + "|#|" + user_name_list[i] + "|#|" + (user_name_list[i] + 'pwd') + "|#|" + \
                            email_address_list[i]
            f.write(write_to_file)


    def delete_account_accesskey(user_name_list):

        for i in range(len(user_name_list)):
            paginator = client.get_paginator('list_access_keys')
            for response in paginator.paginate(UserName=user_name_list[i]):
                AccessKeyMetadata = response['AccessKeyMetadata']
                print(AccessKeyMetadata)
                for AccessKeyId in AccessKeyMetadata:
                    key = AccessKeyId['AccessKeyId']
            response = client.delete_access_key(
                UserName=user_name_list[i],
                AccessKeyId=key
            )
        logger.debug("Success - Deleted account accesskey\n" + str(response))


    def create_login_profile(user_name_list):

        for user_name in user_name_list:
            password = user_name + 'pwd'
            response = client.create_login_profile(
                UserName=user_name,
                Password=password,
                PasswordResetRequired=False
            )
            logger.debug("Success - user login profile created " +
                         str(response))


    def delete_login_profile(user_name_list):
        logger.debug("Number of users in file - " + str(len(user_name_list)))
        for user_name in user_name_list:
            response = client.delete_login_profile(
                UserName=user_name
            )
            logger.debug("Success - Deleted account login profile\n" + str(response))


except client.exceptions.EntityAlreadyExistsException:
    print("User already exists")

except ClientError as e:
    logger.error(e.response['Error']['Message'])

except Exception as err:
    logger.error(err)

