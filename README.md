# aws user management

Utility to manage users in AWS Account, it will come in handy when you need to create a set of users for a specific purpose(training/workshops/seminars) and then delete when done.
The utility performs below functionalities under IAM and SES
- Create AWS IAM group, policy, role, and users
- Assign the policy to a group
- Add users to the group
- Create a login profile for users
- Generate an account access key for programmatic access 
- Send an email to the users with account details

###List of AWS services used:
- IAM
- SES

###Technology/Software Stack:
- Python
- Boto3

###Prerequisite:
- Active AWS account with admin access
- Account access/secret key stored under .aws folder

###Installation steps


## License
None


## Acknowledgments
Stackoverflow for troubleshooting exceptions