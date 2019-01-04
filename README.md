# aws user management

Utility to manage users in AWS Account, it will come in handy when you need to create a set of users for a specific purpose(training/workshops/seminars) and then delete when done.
The utility performs below functionalities under IAM and SES
- Create AWS IAM group, policy, role, and users
- Assign the policy to a group
- Add users to the group
- Create a login profile for users
- Generate an account access key for programmatic access 
- Send an email to the users with account details

## List of AWS services used:
- IAM
- SES

### Technology/Software Stack:
- Python
- Boto3

### Prerequisite:
- Active AWS account with admin access
- Account access/secret key stored under .aws folder
- Python 3.x and pip

### Installation steps
```
git clone https://github.com/marakere/aws-workshop.git
cd aws-workshop
#Create the virual environment
python -m virtualenv venv
#Activate and install the project dependencies
source venv/bin/activate
pip install -r requirements.txt

#Renaming the files to actual file names 
mv input/sample_enrolled_users_identities.txt input/enrolled_users_identities.txt
mv config/sampleconfig.py config/config.py

#Replace the dummy AWS account with actual one
vi config/config.py
—change the policyarn account to a valid AWS account ID


python -m app.create_aws_resources.py
After successful execution, login to was console and verify the email address. Once the email address verification is complete, it’s time to send email with credentials.
vi app/create_aws_resources.py
— Comment all the functions and uncomment send_templated_email() to send out email and run the file again
python -m app.create_aws_resources.py
# By now you should have an email in inbox with login details. 

# Delete the resources created by running the below command
python -m app.delete_aws_resources.py
```

## License
None


## Acknowledgments
Big thank you to StackOverflow in helping to overcome exceptions