import json, base64, gzip, logging, boto3, os, sys
s3 = boto3.client('s3')
ec2 = boto3.client('ec2')
log_level = os.getenv('LOG_LEVEL',20)
logger = logging.getLogger()
logger.setLevel(int(log_level))
def lambda_handler(event, context):
    if event:
        #Mostra todo o evento records e a variavel arquivo recebe o campo RECORDS do json
        print('Evento: ', event)
        arquivo = event["Records"][0]
        #A variavel nomeArquivo recebe o nome do arquivo esta no campo s3/object/key do json
        nomeArquivo = arquivo['s3']['object']['key']
        logger.info(f'Nome do arquivo: {nomeArquivo}' )
         
        #A variavel objeto recebe o arquivo que foi colocado no bucket 
        objeto = s3.get_object(Bucket = 'logs-cloudtrail-666', Key = nomeArquivo)
        logger.debug(f'Objeto recebido do S3: {objeto}') 
        
        #A variavel dadosObjeto recebe o corpo do arquivo json
        dadosObjeto = objeto["Body"].read()
        #A variavel compressed descodifica o arquivo json
        compressed = base64.b64decode(dadosObjeto)
        #A variavel json_payload descomprime o objeto gzip que foi descodificado
        json_payload = gzip.decompress(dadosObjeto)
        logger.debug(f'Informações do arquivo: {json_payload} ')
        logger.info('Arquivo descomprimido com sucesso!')
        #Carrega o arquivo json para dentro de um dicionario
        dicionario_json = json.loads(json_payload)
        
        #Identifica a instancia infectada pelo campo errorCode
        for records in dicionario_json["Records"]:
            #Se o campo errorCode for um erro de operação não autorizada, quer dizer que a instancia está infectada
            if records.get("errorCode", None) == "Client.UnauthorizedOperation":
                #Pega o id da instancia
                instance_id = records["userIdentity"]["principalId"].split(':')[1]
                #Isola a instancia no security group
                response = ec2.modify_instance_attribute(
                    InstanceId = str(instance_id),
                    Groups = ['sg-054e48ff777544754'])
                logger.info(f'ID da instância infectada: {instance_id}')
                logger.info('Instância infectada isolada com sucesso!')
                break