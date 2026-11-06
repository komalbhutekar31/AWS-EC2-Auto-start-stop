AWS EC2 Auto Start/Stop Automation

1. Project Overview

This project automates the starting and stopping of multiple AWS EC2 instances using AWS Lambda, Amazon EventBridge Scheduler, and Python (Boto3).

The main objective is to automate EC2 instance operations according to predefined schedules and reduce unnecessary AWS infrastructure costs.

2. Technologies Used

- AWS EC2
- AWS Lambda
- Amazon EventBridge Scheduler
- Python
- Boto3
- AWS IAM
- CloudWatch Logs

3. Project Architecture

EventBridge Scheduler
|
v
AWS Lambda Function
|
v
Python Boto3 SDK
|
v
AWS EC2 Instances
|
v
Start / Stop Operations

4. Project Implementation

I created automated schedules for five developer EC2 instances.

Developer| Start Time| Stop Time
Dev 1| 6:00 AM| 10:00 AM
Dev 1| 9:00 PM| 1:00 AM
Dev 2| 5:00 PM| 12:00 AM
Dev 3| 2:00 PM| 6:00 PM
Dev 4| 4:00 AM| 8:00 AM
Dev 4| 7:00 PM| 9:00 PM
Dev 5| 1:00 AM| 5:00 AM

5. How It Works

1. EventBridge Scheduler triggers the Lambda function based on configured cron expressions.
2. AWS Lambda executes the Python code.
3. Boto3 communicates with the EC2 service.
4. Based on the scheduled action, the required EC2 instances are started or stopped.
5. CloudWatch Logs help monitor Lambda execution.

6. IAM Permissions

The Lambda execution role requires the following EC2 permissions:

- ec2:DescribeInstances
- ec2:StartInstances
- ec2:StopInstances

CloudWatch Logs permissions are also required for execution monitoring.

7. Benefits

- Reduces manual EC2 management.
- Helps optimize AWS infrastructure costs.
- Automates developer working-hour schedules.
- Improves operational efficiency.
- Provides scheduled infrastructure management.

8. Conclusion

This project helped me gain practical knowledge of AWS Lambda, EventBridge Scheduler, EC2, IAM, Python, and Boto3.

It demonstrates how cloud infrastructure tasks can be automated using serverless AWS services.