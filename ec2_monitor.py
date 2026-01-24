import boto3

ec2 = boto3.client("ec2")

response = ec2.describe_instances()

print("\nEC2 INSTANCE STATUS CHECK\n")

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:

        instance_id = instance["InstanceId"]
        instance_type = instance["InstanceType"]
        state = instance["State"]["Name"]

        public_ip = instance.get("PublicIpAddress")

        print(f"Instance ID   : {instance_id}")
        print(f"Instance Type : {instance_type}")
        print(f"State         : {state}")

        if state == "running":
            print("Cost Status   : RUNNING ")
        else:
            print("Cost Status   : Not running")

        if public_ip:
            print(f"Public IP     : {public_ip}")
            print("SSH Access    : Possible")
        else:
            print("Public IP     : None")
            print("SSH Access    : Not available")

print("\nCheck complete.\n")
