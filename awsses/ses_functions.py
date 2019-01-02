import boto3
from botocore.exceptions import ClientError
from app.read_users_from_file import *
from utils.loggingtemplate import logger
from config import config

try:
    client = boto3.client('ses')

    # read_enrolled_users(config.enrolled_users_file)

    def verify_email_address(filename):
        with open(filename, 'r') as readfile:
            next(readfile)
            for line in readfile:
                first_name, last_name, email_address = line.split('|')
                logger.debug("Email Address to be verified - " + email_address)

                response = client.verify_email_identity(
                    EmailAddress=email_address.lower()
                )
                logger.debug('Success - Verification email sent to ' + email_address + '. Request ID: ' +
                             response['ResponseMetadata']['RequestId'])

    def delete_verified_email_address(filename):
        with open(filename, 'r') as readfile:
            next(readfile)
            for line in readfile:
                first_name, last_name, email_address = line.split('|')
                logger.debug("Email Address to be verification to be deleted - " + email_address)

                response = client.delete_verified_email_address(
                    EmailAddress=email_address.lower()
                )
                logger.debug('Success - Deleted the verification email address  ' + email_address + '. Request ID: ' +
                             response['ResponseMetadata']['RequestId'])

    def create_configuration(configset_name):
        response = client.create_configuration_set(
            ConfigurationSet={
                'Name': configset_name
            }
        )
        logger.debug("configuration created successfully " + str(response))


    def delete_configuration(configset_name):
        response = client.delete_configuration_set(
            ConfigurationSetName=configset_name
        )
        logger.debug("configuration deleted successfully " + str(response))


    def create_template(template_name, subject_content, html_content):
        response = client.create_template(
            Template={
                "TemplateName": template_name,
                "SubjectPart": subject_content,
                "HtmlPart": html_content
            }
        )
        logger.debug("template created successfully " + str(response))

    def delete_template(template_name):
        response = client.delete_template(
            TemplateName=template_name
        )
        logger.debug("template deleted successfully " + str(response))

    def send_templated_email(source_email, template_name, configset_name, email_address_list, template_content):


        updated_template_content = []
        with open('accounts-created.txt', 'r') as readfile:
            for line in readfile:
                awsacccesskey, awssecretkey, firstname, lastname, username, password, emailaddress = line.split('|#|')
                logger.debug("awsacccesskey, awssecretkey, firstname, lastname, username, password, emailaddress")
                logger.debug(str(awsacccesskey), str(awssecretkey), str(firstname), str(lastname), str(username), str(password), str(emailaddress))
                updated_template_content.append(
                    template_content.replace('##', lastname).replace('$$', 'http').replace('**', username).replace('%%',
                        password).replace('@@', awsacccesskey).replace('==', awssecretkey).replace('http', config.aws_console_link))


        for i in range(len(email_address_list)):

            logger.debug("Targeted email address -- " + email_address_list[i])
            logger.debug("Dynamic content for the email -- " + updated_template_content[i])

            response = client.send_templated_email(
                Source=source_email,
                Template=template_name,
                ConfigurationSetName=configset_name,
                Destination={
                    "ToAddresses": [email_address_list[i].lower()
                                    ]
                },
                TemplateData=updated_template_content[i]

            )
            logger.debug("email sent successfully " + str(response))


except ClientError as e:
    logger.error(e.response['Error']['Message'])

except Exception as err:
    logger.error(err)

# read_enrolled_users(config.enrolled_users_file)
# verify_email_address(config.enrolled_users_file)
# create_configuration(config.configset_name)
# create_template(config.template_name, config.subject_content, config.html_content)
# send_templated_email(config.source_email, config.template_name, config.configset_name,
#                     email_address_list, config.generic_template)
