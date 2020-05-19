#!/usr/bin/env python3
import subprocess
from update_disposition import cookie_loader
from update_disposition import upload_file

from ExoFOP import ExoFOP_parameters
import subprocess
from my_targets import my_targets

#filename='ExoFOP_testing_info.txt'
filename='ExoFOP_testing_info2.txt'
params=ExoFOP_parameters(filename)
subprocess.call(['./create_cookie.sh',filename])
#cookies=cookie_loader('exocookies_mlund.txt')
print(params['cookie'])
cookies=cookie_loader(params['cookie'])
print(cookies)
#quit()
#my_targets('mytargets.txt', params['cookie'])

#subprocess.call(['./create_cookie.sh'])
#cookies=cookie_loader('exocookies_mlund.txt')
#bulk_url="https://newphpifop.ipac.caltech.edu/tess/newbulk_upload.php"
#toi_update_file="ml20190606-002.tar"

#submission_text=upload_file(bulk_url, cookies, toi_update_file)
#print submission_text


bulk_param_url="https://exofopdev.ipac.caltech.edu/tess/bulk_upload_params.php"
#bulk_param_url="https://newphpifop.ipac.caltech.edu/tess/bulk_upload_params.php"
update_file="params_stellar_20200421_001.txt"

print(bulk_param_url, cookies)
submission_text=upload_file(bulk_param_url, cookies, update_file)
print(submission_text)

#https://exofopdev.ipac.caltech.edu/tess/bulk_upload_params.php
