import time, os
from botocore.vendored import requests

#Set the filename and open the file
filename = 'app_logs'
team = "MY_TEAM"
refund_endpoint = "http://REFUNDENDPOINT"
file = open(filename,'r')

#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

while 1:
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        print line, # already has newline
        refund = line.split(' ')[6]
        parameter = {'team': f'{team}', 'refund': f'{refund}'}
        response = requests.get(f'{refund_endpoint}',params=parameter)