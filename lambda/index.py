import json, boto3, os

def lambda_handler(event, context):
    print(event)

    method = event['httpMethod']
    path = event['path']

    if method == 'GET':
        if path == '/lambda':
            query_string = event['queryStringParameters']
            for qs in query_string:
                if qs == 'input':
                    value = query_string[qs]
                    client = boto3.client('dynamodb', region_name=os.getenv("AWS_REGION"))
                    response = client.put_item (
                        TableName=os.getenv("TABLE_NAME"),
                        #TableName='input',
                        Item={
                            'id': {
                                'S': value,
                            }
                        }
                    )
                    print(response)
                    return {
                        "statusCode": 200,
                        "statusDescription": "HTTP OK",
                        "isBase64Encoded": False,
                        "headers": {
                            "Content-Type": "text/html"
                        },
                        "body": "OK Insert on Dynamo " + value
                    }                        
    return {
        "statusCode": 500,
        "statusDescription": "Internal Erro",
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": "Internal Erro"
    }