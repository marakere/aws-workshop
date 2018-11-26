import json

import boto3
from botocore.exceptions import ClientError
from app.user_enrollment import *
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


    def create_iam_group(org_path, iam_group_name):

        response = client.create_group(
            Path=org_path,
            GroupName=iam_group_name
        )
        logger.debug("Success - iam group created\n" + str(response))


    def attach_group_policy(policy_arn, org_path, iam_policy_name, iam_group_name):

        new_policy_arn = policy_arn + org_path + iam_policy_name
        response = client.attach_group_policy(
            GroupName=iam_group_name,
            PolicyArn=new_policy_arn
        )
        logger.debug("Success - Attaching the policy to the group\n " + str(response))


    def app_specific_role(iam_role_name, org_path, role_policy_filename):

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


    def create_iam_user(org_path, user_name_list):

        logger.debug("Number of users in file - " + str(len(user_name_list)))
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


    def add_user_to_group(iam_group_name, user_name_list):

        for user_name in user_name_list:
            response = client.add_user_to_group(
                GroupName=iam_group_name,
                UserName=user_name
            )
            logger.debug("Success - Added user to the group " + str(response))


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


except ClientError as e:
    logger.error(e.response['Error']['Message'])

except Exception as err:
    logger.error(err)

logger.debug('Testing the class iam-functions')

# read_enrolled_users(config.enrolled_users_file)
# create_iam_group_policy(config.iam_policy_name, config.org_path, config.policy_filename)
# create_iam_group(config.org_path, config.iam_group_name)
# attach_group_policy(config.policy_arn, config.org_path, config.iam_policy_name, config.iam_group_name)
# app_specific_role(config.iam_role_name, config.org_path, config.role_policy_filename)
# create_iam_user(config.org_path, user_name_list)
# add_user_to_group(config.iam_group_name, user_name_list)
# create_account_accesskey(user_name_list, first_name_list, last_name_list, email_address_list)
# create_login_profile(user_name_list)
