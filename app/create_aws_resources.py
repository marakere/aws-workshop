import json
import boto3
from botocore.exceptions import ClientError
from config import config
from utils.loggingtemplate import logger
from app.read_users_from_file import  read_enrolled_users
from awsiam.iam_functions import *
from awsses.ses_functions import *





try:
    logger.debug("Create AWS IAM and SES resources for the workshop")
    # read_enrolled_users(config.enrolled_users_file)
    # create_iam_group_policy(config.iam_policy_name, config.org_path, config.policy_filename)
    # create_iam_group(config.org_path, config.iam_group_name)
    # attach_group_policy(config.policy_arn, config.org_path, config.iam_policy_name, config.iam_group_name)
    # create_app_specific_role(config.iam_role_name, config.org_path, config.role_policy_filename)
    # create_iam_user(config.org_path, user_name_list)
    # add_user_to_group(config.iam_group_name, user_name_list)
    # create_account_accesskey(user_name_list, first_name_list, last_name_list, email_address_list)
    # create_login_profile(user_name_list)
    # verify_email_address(config.enrolled_users_file)
    # create_configuration(config.configset_name)
    # create_template(config.template_name, config.subject_content, config.html_content)
    send_templated_email(config.source_email, config.template_name, config.configset_name,
                         email_address_list, config.generic_template)

except Exception as err:
    logger.error(err)