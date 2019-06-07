#!/usr/bin/env python
import subprocess
from update_disposition import cookie_loader
from update_disposition import upload_file

subprocess.call(['./create_cookie.sh'])
cookies=cookie_loader('exocookies_mlund.txt')
bulk_url="https://newphpifop.ipac.caltech.edu/tess/newbulk_upload.php"
toi_update_file="ml20190606-002.tar"

submission_text=upload_file(bulk_url, cookies, toi_update_file)
print submission_text
