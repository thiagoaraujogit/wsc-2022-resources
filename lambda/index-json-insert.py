import json, boto3, os

REGION_NAME = os.getenv("AWS_REGION")
TABLE_NAME='lambda'

def lambda_handler(event, context):
    print(event)
    if event['httpMethod'] == 'GET':
      if event['path'] == '/lambda':
        query_strings = event['queryStringParameters']
        if 'input' in query_strings:
          
          itens = {}
          for query in query_strings:
            itens[query] ={'S': query_strings[query]}
          
          print(itens)
          
          client = boto3.client('dynamodb',region_name=REGION_NAME)
          response = client.put_item(
            TableName=TABLE_NAME,
            Item=itens
          )
          print(response)
        else:
          itens = 'Não encontrado a query string input'

        return {
            "statusCode": 200,
            "statusDescription": "HTTP OK",
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "application/json; charset=utf-8"
            },
            "body": json.dumps(itens)
        } 
