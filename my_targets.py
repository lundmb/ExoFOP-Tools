#!/usr/bin/env python3
from bs4 import BeautifulSoup
#import cookielib
#import requests
#import time
from update_disposition import cookie_loader
from update_disposition import upload_file
from ExoFOP import ExoFOP_parameters
import subprocess

def my_targets(filename, cookie_string, submission_url, output_location=None):
   #cookies=cookie_loader('exocookies_mlund.txt')
   #url='https://newphpifop.ipac.caltech.edu/tess/mytargets_upload.php'
   #cookies=cookie_loader('exocookies_mlund_live.txt')
   cookies=cookie_loader(cookie_string)
   #url='https://exofop.ipac.caltech.edu/tess/mytargets_upload.php'
   print(submission_url, cookies, filename)
   #return("ERROR")
   output=upload_file(submission_url, cookies, filename)
   print(output)
   

if __name__ == "__main__":
   import sys
   print(sys.argv[1], sys.argv[2])
   params=ExoFOP_parameters(sys.argv[2])
   print(params)
   #quit()
   subprocess.call(['./create_cookie.sh',sys.argv[2]])
   my_targets(sys.argv[1], params['cookie'])

#'exocookies_mlund.txt' for test
#'exocookies_mlund_live.txt' for live


#   files = {'file_name': (filename, open(filename, 'rb')),}
#cookies = {
#}
#
#files = {
#    'file_name': ('mytargets.txt', open('mytargets.txt', 'rb')),
#}
#
#response = requests.post('https://newphpifop.ipac.caltech.edu/tess/mytargets_upload.php', cookies=cookies, files=files)
