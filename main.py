import pywren_ibm_cloud as pywren
import time
import re

N_SLAVES = 100
BUCKET_NAME = 'urvbucket'

# Configuracio del ibm cloud
config = {'pywren' : {'storage_bucket' : BUCKET_NAME},

          'ibm_cf':  {'endpoint': 'https://eu-gb.functions.cloud.ibm.com', 
                      'namespace': 'adria.ribas@estudiants.urv.cat_dev', 
                      'api_key': 'c4b8698b-aa44-4a49-a6f0-b231f9cfd2ae:I8oY3vVJeZOIc0TEP1dJmeHO3o1ZV7jCDPwmPvakzpMc3vrdmgYmWtTDLqmoyHjQ'}, 

          'ibm_cos': {'endpoint': 'https://s3.eu-gb.cloud-object-storage.appdomain.cloud',
                      'private_endpoint': 'https://s3.private.eu-gb.cloud-object-storage.appdomain.cloud',
                      'api_key': '-k3E4W-hzX4YaWW_Dopxem1MuPQciEMJNFIsIVv-yFUQ'}}

# Funcio master
def master(id, x, ibm_cos):

    write_permission_list = []

    res = 0
    while (res != 200):
        try:
            res = ibm_cos.put_object(Bucket=BUCKET_NAME, Key='result.txt')['ResponseMetadata']['HTTPStatusCode']
        except:
            time.sleep(0.5)

    while (True):
        # 1. monitor COS bucket each X seconds
        time.sleep(2)

        # 2. List all "p_write_{id}" files
        try:
            write_request_list = ibm_cos.list_objects(Bucket=BUCKET_NAME, Prefix='p_write_')['Contents']
        except:
            break
            
        # 3. Order objects by time of creation
        write_request_list.sort(key=lambda x: x['LastModified'])

        while (len(write_request_list) > 0):

            # 4. Pop first object of the list "p_write_{id}"
            first_write_request = write_request_list.pop(0)
            id = int(re.search(r'\d+', first_write_request['Key']).group())

            # 5. Write empty "write_{id}" object into COS
            result_md5 = ibm_cos.get_object(Bucket=BUCKET_NAME, Key='result.txt')['ETag']

            res = 0
            while (res != 200):
                try:
                    res = ibm_cos.put_object(Bucket=BUCKET_NAME, Key='write_{' + str(id) + '}')['ResponseMetadata']['HTTPStatusCode']
                except:
                    time.sleep(0.5)

            # 6. Delete from COS "p_write_{id}", save {id} in write_permission_list
            ibm_cos.delete_object(Bucket=BUCKET_NAME, Key='p_write_{' + str(id) + '}')
            write_permission_list.append('{' + str(id) + '}')

            # 7. Monitor "result.json" object each X seconds until it is updated
            while (result_md5 == ibm_cos.get_object(Bucket=BUCKET_NAME, Key='result.txt')['ETag']):
                time.sleep(0.5)
            
            # 8. Delete from COS “write_{id}”
            ibm_cos.delete_object(Bucket=BUCKET_NAME, Key='write_{' + str(id) + '}')
            
        # 8. Back to step 1 until no "p_write_{id}" objects in the bucket

    return write_permission_list

# Funcio slave
def slave(id, x, ibm_cos):

    # 1. Write empty "p_write_{id}" object into COS
    res = 0
    while (res != 200):
        try:
            res = ibm_cos.put_object(Bucket=BUCKET_NAME, Key='p_write_{' + str(id) + '}')['ResponseMetadata']['HTTPStatusCode']
        except:
            time.sleep(0.5)

    # 2. Monitor COS bucket each X seconds until it finds a file called "write_{id}"
    while (True):
        try:
            ibm_cos.get_object(Bucket=BUCKET_NAME, Key='write_{' + str(id) + '}')
            break
        except:
            time.sleep(0.5)

    # 3. If write_{id} is in COS: get result.txt, append {id}, and put back to COS result.txt
    try:
        result = ibm_cos.get_object(Bucket=BUCKET_NAME, Key='result.txt')['Body'].read().decode()
    except:
        res = 0
        while (res != 200):
            try:
                res = ibm_cos.put_object(Bucket=BUCKET_NAME, Key='result.txt')['ResponseMetadata']['HTTPStatusCode']
            except:
                time.sleep(0.5)
                result = ''
    
    result = result + '{' + str(id) + '}'

    res = 0
    while (res != 200):
        try:
            res = ibm_cos.put_object(Bucket=BUCKET_NAME, Key='result.txt', Body=result.encode())['ResponseMetadata']['HTTPStatusCode']
        except:
            time.sleep(0.5)

    # 4. Finish
    # No need to return anything

# Funcio buidar bucket
def emptyBucket(id, x, ibm_cos):

    for objecte in ibm_cos.list_objects(Bucket=BUCKET_NAME)['Contents']:
        ibm_cos.delete_object(Bucket=BUCKET_NAME, Key=objecte['Key'])

# Funcio main
if __name__ == '__main__':
    pw = pywren.ibm_cf_executor(config=config)
    pw.call_async(master, 0)
    pw.map(slave, range(N_SLAVES))
    write_permission_list = pw.get_result()

    # Get result.txt
    results = pw.internal_storage.get_client().get_object(Bucket=BUCKET_NAME, Key='result.txt')['Body'].read().decode()

    # check if content of result.txt == write_permission_list
    print('master:\t\t', end='')

    write_permission_string = ''

    for result in write_permission_list[0]:
        write_permission_string = write_permission_string + result
        print(result, end='')

    print('\nresult.txt:\t' + results)

    if (results == write_permission_string):
        print("Els resultats son correctes")

    # Empty bucket
    pw.call_async(emptyBucket, 0)