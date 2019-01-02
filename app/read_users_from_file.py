import json

import boto3
from botocore.exceptions import ClientError

from utils.loggingtemplate import logger

first_name_list = []
last_name_list = []
email_address_list = []
user_name_list = []

try:
    def read_enrolled_users(filename):
        with open(filename, 'r') as readfile:
            next(readfile)
            for line in readfile:
                first_name, last_name, email_address = line.split('|')
                first_name_list.append(first_name)
                last_name_list.append(last_name)
                email_address_list.append(email_address)
                user_name_list.append(generate_username(first_name, last_name))
                logger.debug(
                    "Firstname - " + first_name + " Lastname - " + last_name + " Emailaddress - " + email_address)


    def generate_username(first_name, last_name):
        user_name = first_name[0].lower() + last_name.lower()
        logger.debug("Concatenate first + last name - " + user_name)
        return user_name

except FileNotFoundError as err:
    logger.error(err)

except Exception as err:
    logger.error(err)