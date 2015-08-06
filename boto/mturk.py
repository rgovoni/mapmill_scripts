import time

def get_keys_and_host(keys_file, production):
    access_key_id = None
    secret_key = None

    with open(keys_file, 'r') as keys:
        for line in keys.xreadlines():
            items = [xx.strip() for xx in line.split('=')]
            if items[0] == 'AWSAccessKeyId':
                access_key_id = items[1]
            elif items[0] == 'AWSSecretKey':
                secret_key = items[1]

    if not access_key_id or not secret_key:
        raise RuntimeError('Invalid keys file format.')



    if production:
        print '*** Using production host! ***'
        time.sleep(2)
        print '.'
        time.sleep(2)
        print '.'
        time.sleep(2)
        print '.'
        time.sleep(2)
        
        host = 'mechanicalturk.amazonaws.com'
    else:
        print 'Using sandbox host.'

        host = 'mechanicalturk.sandbox.amazonaws.com'



    return access_key_id, secret_key, host
