from awsiam.iam_functions import *
from awsses.ses_functions import *

try:
    logger.debug("Delete AWS IAM and SES resources created for the workshop")
    # read_enrolled_users(config.enrolled_users_file)

    delete_configuration(config.configset_name)
    delete_template(config.template_name)
    delete_verified_email_address(config.enrolled_users_file)
    delete_login_profile(user_name_list)
    remove_user_from_group(config.iam_group_name, user_name_list)
    delete_account_accesskey(user_name_list)
    delete_iam_user(user_name_list)
    detach_group_policy(config.policy_arn, config.org_path, config.iam_policy_name, config.iam_group_name)
    delete_iam_group_policy(config.policy_arn, config.org_path, config.iam_policy_name)
    delete_app_specific_role(config.iam_role_name)
    delete_iam_group(config.iam_group_name)

except Exception as err:
    logger.error(err)
