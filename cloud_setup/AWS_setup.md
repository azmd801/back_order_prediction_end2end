# AWS Setup
The AWS Setup Guide is a step-by-step resource for creating key AWS services, such as IAM users, S3 buckets, ECR repositories, and EC2 instances.

## 1. Create AWS Account:

- If you don't have an AWS account, sign up [here](https://aws.amazon.com/) and attach a credit card.
- Log in to your AWS account.

## 2. IAM (Identity and Access Management):

### 2.1. Create IAM User:

- In the AWS Management Console, use the search bar and type "IAM."
- Click on "IAM" to navigate to the Identity and Access Management (IAM) console.
- Within IAM, click on "Users" and then "Add user."
- Enter a username (e.g., "ml-user") and select "Programmatic access."
- Proceed to the next permissions step.
- Choose "Attach existing policies directly" and select the following policies:
  - `AmazonEC2FullAccess`
  - `AmazonEC2ContainerRegistryFullAccess`
  - `AmazonS3FullAccess`
- Continue to the next steps (tags, review), skipping tags if not needed.
- Review the user's permissions and details, then click "Create user."

### 2.2. Download AWS Credentials:

- Once the user is created, download the CSV file containing the credentials.
- Safeguard the AWS access key ID and secret access key; keep them secure and do not share them.
- Be cautious as there is no way to retrieve lost credentials.

## 3. S3 (Simple Storage Service):

### 3.1. Create S3 Bucket:

- In the AWS Management Console, use the search bar and type "S3."
- Click on "S3" to navigate to the Simple Storage Service (S3) console.
- Click on "Create bucket."
- Provide a unique name for the bucket, e.g., "model."
- Choose a region for the bucket.
- Optionally, configure advanced settings like versioning, logging, and tags.
- Click through the remaining steps, leaving other settings as default.
- Review the configuration and click "Create bucket."


## 4. ECR (Elastic Container Registry):

### 4.1. Create ECR Repository:

- In the AWS Management Console, use the search bar and type "ECR."
- Click on "ECR" to navigate to the Elastic Container Registry (ECR) console.
- Click on "Create repository."
- Provide a repository name and configure repository settings.
- Optionally, configure lifecycle policies for image cleanup.
- Click "Create repository."

## 5. EC2 (Elastic Compute Cloud) Instance:

### 5.1. Launch EC2 Instance:

- In the AWS Management Console, use the search bar and type "EC2."
- Click on "EC2" to navigate to the Elastic Compute Cloud (EC2) console.
- Click on "Instances" and then "Launch Instance."
- Choose an Amazon Machine Image (AMI) based on your requirements.
- Select an instance type, configure instance details, add storage, and configure security groups.
- Review configurations and launch the instance.


