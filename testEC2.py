#!/usr/bin/python
# poll the AWS Trusted Advisor for resource limits and posts an SNS message to a topic with AZ and resource information
# Import the SDK
import boto3
import uuid
import json
import ConfigParser
from boto3 import Session
from datetime import datetime

def json_serial(obj):
	if isinstance(obj, datetime):
		serial = obj.isoformat()
		return serial
	raise TypeError ("Type not serializable")

ec2_client = boto3.client('ec2', 'us-west-2')


##############
#get RI information for rgn
##############

response = ec2_client.describe_reserved_instances()
ri_list = ri_response['ReservedInstances']
i = 0
ri_az = []
ri_type = []
ri_count = []
for ri in ri_list:
	ri_az.append(ri['AvailabilityZone'])
	ri_type.append(ri['InstanceType'])
	ri_count.append(ri['InstanceCount'])
	print 'RI values: '+ri_az[i], ri_type[i], str(ri_count[i])
	i += 1
print "RI Value:"
print json.dumps(ri_response, indent=4, separators=(',', ': '), default=json_serial)


###############
#call EC2 stats for rgn
###############
response = ec2_client.describe_instances()
reservation_list = response['Reservations']
num_of_instances = 0
ri_match = 0

for rsrv in reservation_list:
	#if instance matches RI requirements, add to new list
	instance_list = rsrv['Instances']
	instance_id = rsrv['Instances'][0]['InstanceId']
	instance_type = rsrv['Instances'][0]['InstanceType']
	avail_zone = rsrv['Instances'][0]['Placement']['AvailabilityZone']
	if avail_zone == ri_az[x] and instance_type == ri_type[x]:
		ri_match += 1
	num_of_instances += 1
	print 'Instance number:'+ str(num_of_instances)
	print instance_id
	print instance_type
	print avail_zone
	print '------'
	# print json.dumps(instance_list, indent=4, separators=(',', ': '), default=json_serial)

print "Number of instances that match your RI: " + ri_match



