import json, base64, gzip, logging, boto3, os, sys

s3 = boto3.client('s3')
ec2 = boto3.client('ec2')
db = boto3.client('dynamodb')
log_level = os.getenv('LOG_LEVEL',20)
logger = logging.getLogger()
logger.setLevel(int(log_level))

def lambda_handler(event, context):
    print('Evento: ', event)
    evento = event['awslogs']['data']
    logging.debug(f'Arquivo codificado: {evento}')
    decodificar = base64.b64decode(evento)
    logging.debug(f'Arquivo decodificado: {decodificar}')
    compressed = gzip.decompress(decodificar)
    logging.debug(f'Arquivo descomprimido: {compressed}')
    
    json_arquivo = json.loads(compressed)
    
    instance_id = json_arquivo['logStream']
    logging.debug(f'ID da instância: {instance_id}')
    
    for log_message in json_arquivo['logEvents']:
        log = log_message.get('message', None)
        log = log.split(' ')
        if log[0] == 'the':
            log = log[3]
            logging.debug(f'LOG: {log}')
            response = db.put_item(
                TableName='logs',
                Item={
                    'codigo': {
                        'S': f'{log} / {instance_id}'
                    }
                }
                )
        else:
            log = log[0]
            logging.debug(f'LOG: {log}')
            response = db.put_item(
                TableName='logs',
                Item={
                    'codigo': {
                        'S': f'{log} / {instance_id}'
                    }
                }
                )
        break