import json, os, sys, boto3, logging

log_level = os.getenv('LOG_LEVEL',20)
logger = logging.getLogger()
logger.setLevel(int(log_level))
cache = boto3.client('elasticache')

def lambda_handler(event, context):
    print(f'Evento: {event}')
    
    #Describes the Memcache Cluster
    current_cluster = cache.describe_cache_clusters(
        CacheClusterId='test-memcache-elc'
    )
    
    #Get the amount of nodes than have on cluster and adds 1 node
    logging.debug(f'Return: {current_cluster}')
    node_number = current_cluster['CacheClusters'][0]['NumCacheNodes']
    logging.debug(f'Number of nodes: {node_number}')
    node_number += 1
    
    new_node = cache.modify_cache_cluster(
        CacheClusterId='test-memcache-elc',
        NumCacheNodes=node_number,
        ApplyImmediately=True,
        AZMode='cross-az'
    )
    logging.debug(f'New number of nodes (Increase): {node_number}')
    logging.info('New node added to Memcache Cluster! Success!')