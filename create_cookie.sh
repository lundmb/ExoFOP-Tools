#!/bin/bash

#source ExoFOP_info.txt
source ExoFOP_testing_info.txt
## sourced file needs to contain the following:
## username=[username]
## password=[password]
## url=https://exofop.ipac.caltech.edu/tess/password_check.php
## 

echo $username
echo $password
cookie_name=exocookies_$username$status.txt
echo $cookie_name

curl -v -b ./$cookie_name -c ./$cookie_name --data "username=$username&password=$password&ref=login_user&ref_page=/tess/" $url

sed -i -e 's/#HttpOnly_//g' $cookie_name
# get exit status
res=$?
if [ $res -ne 0 ]; then
    echo "Curl failed with exit code: $res"
else
    echo "Curl: Login succeeded."
fi
