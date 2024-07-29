# The N.A.M.A. Toolbox for AWS

The N.A.M.A. Toolbox will help you get started on Amazon Web Services (AWS) and validate your startup idea quickly with easy to use templates.

N.A.M.A. stands for No-code + AI + Microservices + APIs.

Included are resources to quickly build the the following prototypes using CloudFormation templates, frontend code and backend Lambda function code:

1. No-code Landing Page
2. The Waiting List prototype
3. The Wizard of Oz prototype
4. The Frankenstein prototype

The N.A.M.A. Toolbox assets contained here were created to accompany the content series [MVP Lab on YouTube by Basil Fateen](https://www.youtube.com/@MVPLab-AWS).

Frontend code is developed using plain HTML, JavaScript and CSS. Backend code is developed using either NodeJS or Python, depending on the prototype.

> [!IMPORTANT]
>Any resources created on your AWS account by the CloudFormation scripts may potentially exceed your 'Free Tier' subscription, so don't forget to set up and monitor your billing alerts.

## No-code Landing Page

The goal of this prototype is to create a simple startup landing page with NO-CODE using Wordpress on Lightsail and Airtable to collect user information by embedding a form.

This prototype is referenced in 'No-code for Non-techies' episode here:

[![MVP Lab ep3](https://img.youtube.com/vi/UqzTAyB0gFk/0.jpg)](https://www.youtube.com/watch?v=UqzTAyB0gFk)

### AWS Services utilized: ###

- Lightsail

## The Waiting List prototype

The goal of this prototype is to create a basic landing page to collect private beta signups, to test demand in the market before building the MVP.

In the included sample, our startup is a pet matching service looking for early testers to sign up.

<img width="873" alt="waitinglist-prototype-architecture-diagram" src="https://github.com/user-attachments/assets/b077bbb8-e765-4681-8933-5ed4bff34388">

### AWS Services utilized: ###

- Simple Storage Service (S3)
- Lambda
- DynamoDB
- API Gateway

## The Wizard of Oz prototype

The goal of this prototype is to simuate functionality manually first, to test the potential user experience before automating the functionality using code for the MVP.

In the included sample, our startup analyzes and transforms documents. The user uploads a document, it is placed into a bucket and the administrator recieves a notification about the location of the uploaded file and the email of the user. Now they can simulate the action (reviewing a resume for example) and manually send back the information to the user.

<img width="859" alt="wizardoz-prototype-architecture-diagram" src="https://github.com/user-attachments/assets/cadc9181-0e34-4d97-b820-7746d5b749f6">

### AWS Services utilized: ###

- Simple Storage Service (S3)
- Lambda
- DynamoDB
- API Gateway
- Simple Notification Service (SNS)
- Cognito
  
## The Frankenstein prototype

The goal of this prototype is to test the technical feasibility of the core feature of the MVP first using a Microservice function, before building out the rest of the MVP.

In the included sample, we are now using Generative AI (Claude via Bedrock) to analyze the text of a resume for a specific job an return the relevancy score and analysis to the user in seconds.

<img width="861" alt="frankenstein-prototype-architecture-diagram" src="https://github.com/user-attachments/assets/2069f7c2-c6c6-4088-8d14-1c254f61ed45">

### AWS Services utilized: ###

- Simple Storage Service (S3)
- Lambda
- Bedrock

** Optional services to be combined: **

- Relational Database Service (RDS)
- API Gateway
- Simple Notification Service (SNS)
- Cognito
