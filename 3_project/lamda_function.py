import json
import boto3


# Create SQS client
sqs = boto3.client('sqs')

myQueueUrl='https://sqs.us-east-2.amazonaws.com/166395079358/Rpi.fifo'

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    print("time = " + event['time'])
    print("tclast = " + event['TClast'])
    print("tcavg = " + event['TCavg'])
    print("tchigh = " + event['TChigh'])
    print("tclow = " + event['TClow'])
    print("tflast = " + event['TFlast'])
    print("tfavg = " + event['TFavg'])
    print("tfhigh = " + event['TFhigh'])
    print("tflow = " + event['TFlow'])
    print("hlast = " + event['Hlast'])
    print("havg = " + event['Havg'])
    print("hhigh = " + event['Hhigh'])
    print("hlow = " + event['Hlow'])
    

    
    response = sqs.send_message(
        QueueUrl=myQueueUrl,
        MessageGroupId="messageGroup1",
        MessageBody=(
            '{"time": "'+event['time']+'", "TClast": "'+event['TClast']+'", "TCavg": "'+event['TCavg']+'", "TChigh": "'+event['TChigh']+'", "TClow": "'+event['TClow']+'", "TFlast": "'+event['TFlast']+'", "TFavg": "'+event['TFavg']+'", "TFhigh": "'+event['TFhigh']+'", "TFlow": "'+event['TFlow']+'", "Hlast": "'+event['Hlast']+'", "Havg": "'+event['Havg']+'", "Hhigh": "'+event['Hhigh']+'", "Hlow": "'+event['Hlow']+'"}'
        )
    )
    
    print(response['MessageId'])
    
    return event['time']  # Echo back the first key value
    #raise Exception('Something went wrong')
