import os

root_dir = os.path.dirname(os.path.abspath(__file__))
print(root_dir)
org_path = '/company/awsworkshop/'
iam_group_name = 'company-aws-workshop'
policy_filename = os.path.join(root_dir, 'group_permissions.json')

iam_policy_name = 'workshop-limited-access'
iam_role_name = 'workshop-apigateway-lambda-dynamodb'
policy_arn = 'arn:aws:iam::1234567890:policy'
aws_console_link = 'https://company.signin.aws.amazon.com/console'
role_policy_filename = os.path.join(root_dir, 'lambda_apigateway_role.json')
enrolled_users_file = os.path.join(root_dir, '../input/enrolled_users_identities.txt')
accounts_created_file = os.path.join(root_dir, '../output/accounts-created.txt')
source_email = 'source@gmail.com'

configset_name = 'newconfigset1'
template_name = 'template1'
subject_content = "Greetings, {{name}}!"
html_content = "<h1>Hello {{name}},</h1>" \
               "<p>Thank you for registering to aws-workshop.</p>" \
               "<p>Below are your AWS account details for the workshop<br>" \
               "AWS web console link - {{awswebconsolelink}}<br>" \
               "username - {{username}}<br>" \
               "password - {{password}}<br>" \
               "<br></p>" \
               "<p>Programmatic access <br>" \
               "aws_access_key_id = {{awsacccesskey}} <br>" \
               "aws_secret_access_key = {{awssecretkey}} <br></p>" \
               "<p>If you have any questions, please feel free to reach out to us @ awesome@awesome.com<br>" \
               "<br> Regards,<br> Awesome Team </p>"

generic_template = "{ \"name\":\"##\", \"awswebconsolelink\":\"$$\",\"username\":\"**\", \"password\":\"%%\", \"awsacccesskey\":\"@@\",\"awssecretkey\":\"==\" }"


def test():
    print("All good in the config file")
