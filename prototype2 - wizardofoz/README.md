#wizardoz-cloudformation-template.yaml

How to use this template:

1. Go to the AWS CloudFormation console.
2. Click "Create stack" and upload the template file.
3. Review and create the stack.

After the stack is created:

1. Replace 'YOUR_API_GATEWAY_ENDPOINT' in the html file with the actual endpoint URL from your API Gateway (you can find this in the Outputs section of your CloudFormation stack).


#wizardoz-user-pool-cloudformation.yaml

How to use this template:

1. Go to the AWS CloudFormation console.
2. Click "Create stack" and upload the template file.
3. You'll be prompted to provide a value for CognitoDomainPrefix. This must be globally unique across AWS.
4. Review and create the stack.

After the stack is created:

1. Replace http://localhost/ in the CallbackURLs and LogoutURLs with your actual application URLs before using this in production. This should be the URL of the upload html page from the previous stack (so now it is available only for those who are logged in).

2. The Hosted UI is now configured with the default settings. You may want to customize it further based on your specific requirements.

