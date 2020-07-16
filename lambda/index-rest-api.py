import json, boto3, os

REGION_NAME = os.getenv("AWS_REGION")
TABLE_NAME = 'usuarios'

def lambda_handler(event, context):
  
  print(json.dumps(event))
  
  client = boto3.client('dynamodb',region_name=REGION_NAME)
  
  method = event['httpMethod']
  path = event['path']
  query = event['queryStringParameters']
  body = ''
  if event['body']:
    body = json.loads(event['body'])
  
  response = 'null'
  
  if method == 'GET':
    if path == '/usuario':
      if 'id' in query:
        
        response = client.get_item(
          TableName=TABLE_NAME,
          Key={'id':{'S': query['id']}},
        )
        print(response)
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code == 200:
          body_response = response['Item']
        
  elif method == 'POST':
    if path == '/usuario' and body:
      if 'id' in body:
        itens = {}
        for param in body:
          itens[param] = {'S': body[param]}
          
          response = client.put_item(
            TableName=TABLE_NAME,
            Item=itens
          )
          print(response)
          status_code = response['ResponseMetadata']['HTTPStatusCode']
          
          if status_code == 200:
            body_response = 'success'
          else:
            body_response = 'fail'
        
  return {
    "statusCode":status_code,
    "headers":{
      "Content-Type":"application/json",
    },
    "body": json.dumps(body_response),
  }