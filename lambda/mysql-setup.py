import json
import logging
import os, sys
import boto3
import pymysql
import base64
from botocore.exceptions import ClientError

log_level = os.getenv('LOG_LEVEL',20)
logger = logging.getLogger()
logger.setLevel(int(log_level))
secret_properties = os.getenv('secret_properties')

def lambda_handler(event, context):
  json_payload = json.loads(secret_properties)
  sqlHost = json_payload['sqlHost']
  sqlUser = json_payload['sqlUser']
  sqlDatabase = json_payload['sqlDatabase']

  secret_name = json_payload['RDSSecretID']
  region_name = json_payload['RegionName']

  # Create a Secrets Manager client
  session = boto3.session.Session()
  client = session.client(
      service_name='secretsmanager',
      region_name=region_name
  )

  try:
      get_secret_value_response = client.get_secret_value(
          SecretId=secret_name
      )
  except ClientError as e:
      if e.response['Error']['Code'] == 'DecryptionFailureException':
          # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
          # Deal with the exception here, and/or rethrow at your discretion.
          raise e
      elif e.response['Error']['Code'] == 'InternalServiceErrorException':
          # An error occurred on the server side.
          # Deal with the exception here, and/or rethrow at your discretion.
          raise e
      elif e.response['Error']['Code'] == 'InvalidParameterException':
          # You provided an invalid value for a parameter.
          # Deal with the exception here, and/or rethrow at your discretion.
          raise e
      elif e.response['Error']['Code'] == 'InvalidRequestException':
          # You provided a parameter value that is not valid for the current state of the resource.
          # Deal with the exception here, and/or rethrow at your discretion.
          raise e
      elif e.response['Error']['Code'] == 'ResourceNotFoundException':
          # We can't find the resource that you asked for.
          # Deal with the exception here, and/or rethrow at your discretion.
          raise e
  else:
      # Decrypts secret using the associated KMS CMK.
      # Depending on whether the secret is a string or binary, one of these fields will be populated.
      if 'SecretString' in get_secret_value_response:
          secret = get_secret_value_response['SecretString']
      else:
          decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
   
  secret_pass = json.loads(secret)

  # Connect to the database
  connection = pymysql.connect(
      host = sqlHost,
      user = sqlUser,
      password = secret_pass['password'],
      db = sqlDatabase,
      charset = 'utf8mb4',
      cursorclass = pymysql.cursors.DictCursor
  )

  try:
      with connection.cursor() as cursor:
          # Create table
          sql = "CREATE TABLE IF NOT EXISTS unicorns(unicornid varchar(100), unicornlocation varchar(100))"
          cursor.execute(sql)
          logger.info('Table "unicorns" created with success!')

  except pymysql.Error as e:
      logger.fatal(f'Error: {e}')

  finally:
      connection.close()