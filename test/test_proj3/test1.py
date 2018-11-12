#!/usr/bin/python


import boto3
import json


max_queue_messages = 10
message_bodies = []

region_name = 'us-east-2'
aws_access_key_id = 'AKIAJP6AFUMBOWK2ZPYA'
aws_secret_access_key = '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'
myQueueUrl='https://sqs.us-east-2.amazonaws.com/166395079358/Rpi.fifo'


sqs = boto3.resource('sqs', region_name=region_name,
		aws_access_key_id=aws_access_key_id,
		aws_secret_access_key=aws_secret_access_key)

queue = sqs.Queue(myQueueUrl)

'''
message = queue.receive_messages(
    MaxNumberOfMessages=10,
    WaitTimeSeconds=1)    


#message_bodies.append(body)

#print(message.body)
for msg in message:
	body = json.loads(msg.body)
	print(body['data'])
	
	response = client.delete_message(
    QueueUrl='string',
    ReceiptHandle='string'
)
'''

      
while True:
	messages_to_delete = []
	
	message = queue.receive_messages(
		MaxNumberOfMessages=10,
		WaitTimeSeconds=1)  
	
	for msg in message:
		# process message body
		body = json.loads(msg.body)
		message_bodies.append(body['data'])
		print(body['data'])
		print(body['time'])
		
		with open('data.txt', 'a') as outfile:
			json.dump(body, outfile, sort_keys=True, indent=4)
			outfile.write('\n')
		
		# add message to delete
		messages_to_delete.append({
			'Id': msg.message_id,
			'ReceiptHandle': msg.receipt_handle
		})

	# if you don't receive any notifications the
	# messages_to_delete list will be empty
	if len(messages_to_delete) == 0:
		break
	# delete messages to remove them from SQS queue
	# handle any errors
	else:
		delete_response = queue.delete_messages(
			Entries=messages_to_delete)
			
