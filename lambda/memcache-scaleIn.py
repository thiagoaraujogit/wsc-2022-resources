import boto3, json, logging, os, sys, base64, random

log_level = os.getenv('LOG_LEVEL',20)
logger = logging.getLogger()
logger.setLevel(int(log_level))
cache = boto3.client('elasticache')

def lambda_handler(event, context):
    print(f'Event: {event}')
    
    #Describes the Memcache Cluster
    current_cluster = cache.describe_cache_clusters(
        CacheClusterId='test-memcache-elc',
        ShowCacheNodeInfo=True
    )
    
    logging.debug(f'Cluster Return: {current_cluster}')

    #Get the amount of nodes than have on cluster
    node_number = current_cluster['CacheClusters'][0]['NumCacheNodes']
    logging.debug(f'Number of nodes: {node_number}')
    logging.debug(f'Nodes Return: {describe_nodes}')
    nodes = current_cluster['CacheClusters'][0]
    final_nodes = list()
    
    #Each node id contained in cluster are added to a list 
    for cache_nodes in nodes['CacheNodes']:
        final_nodes.append(cache_nodes['CacheNodeId'])
    logging.debug(f'NODES ID: {final_nodes}')
    
    #Get the amount of nodes than have on cluster and removes 1
    node_number = current_cluster['CacheClusters'][0]['NumCacheNodes']
    node_number -= 1

    #Verify if cluster greater than 2 nodes, if have it, the last cluster added is removed
    #If not, do nothing, because the amount of nodes cannot be smaller than 2 (Multi-AZ)
    if(len(final_nodes) > 2):
        remove_nodes = cache.modify_cache_cluster(
            CacheClusterId='test-memcache-elc',
            NumCacheNodes=node_number,
            CacheNodeIdsToRemove=[ f'{final_nodes[-1]}' ],
            ApplyImmediately=True
        )
        
        logging.info(f'REMOVED NODE: {final_nodes[-1]}')
        logging.info(f'New number of nodes (Decrease): {node_number}')
    else:
        logging.debug("Is not possible to remove a node, the minimum is 2!")