# Import the AWS SDK for Python.
# boto3 lets Python talk to AWS services like EC2, S3, IAM, etc.
import boto3

# Create an EC2 client.
# Think of this as creating a "remote control" object for the EC2 service.
# boto3 will use your configured AWS credentials and default region (from aws configure).
ec2 = boto3.client("ec2")

# Call the EC2 API to fetch information about your instances.
# describe_instances returns a big nested dictionary (JSON-like structure).
# The result is stored in the variable "response".
response = ec2.describe_instances()

# Print a heading so the output is easy to read.
# "\n" adds a new line before and after the text.
print("\nEC2 INSTANCE STATUS CHECK\n")

# AWS groups returned instances inside "Reservations".
# response["Reservations"] is a LIST of reservations.
# We loop through each reservation one by one.
for reservation in response["Reservations"]:

    # Each reservation contains a LIST of EC2 instances under the key "Instances".
    # We loop through each instance in that reservation.
    for instance in reservation["Instances"]:

        # Get the unique instance ID, like: i-0abc1234567890def
        # This key always exists for EC2 instances.
        instance_id = instance["InstanceId"]

        # Get the instance type, like: t3.micro, t2.micro, m5.large, etc.
        instance_type = instance["InstanceType"]

        # Get the instance state (running, stopped, pending, terminated, etc.)
        # "State" is a dictionary, and the actual readable state is in ["Name"].
        state = instance["State"]["Name"]

        # Try to get the public IP address.
        # Some instances DO NOT have a public IP (private subnet or stopped).
        # Using .get() avoids a KeyError if "PublicIpAddress" does not exist.
        public_ip = instance.get("PublicIpAddress")

        # Print instance details using f-strings.
        # f-strings let you insert variables directly into text using {variable}.
        print(f"Instance ID   : {instance_id}")
        print(f"Instance Type : {instance_type}")
        print(f"State         : {state}")

        # If the instance state is "running", it is actively consuming compute and can cost money.
        # If it's not running (stopped, terminated, etc.) compute charges are not active.
        if state == "running":
            print("Cost Status   : RUNNING ")
        else:
            print("Cost Status   : Not running")

        # If there is a public IP, you can potentially SSH into it (if security group allows port 22).
        # If there is no public IP, you cannot SSH from the public internet.
        if public_ip:
            print(f"Public IP     : {public_ip}")
            print("SSH Access    : Possible")
        else:
            print("Public IP     : None")
            print("SSH Access    : Not available")

# Print a final message when the script finishes scanning all instances.
print("\nCheck complete.\n")
