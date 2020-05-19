#!/usr/bin/env python3
from bs4 import BeautifulSoup
import http.cookiejar as cookielib
import requests
import time

def cookie_loader(filename):
   #sh create_cookie.sh was run before here, and then fixed by removing http_only and changing 0 to white space
   cj=cookielib.MozillaCookieJar(filename)
   cj.load(ignore_discard=True, ignore_expires=True)
   for cookie in cj:
      cookie.expires = time.time() + 14*24*3600
   if len(cj) != 1: # must be one
      print("error in cookie")
      quit()
   cookies=cj
   return cookies

def upload_file(url, cookies, filename, verify='on'):
   files = {'file_name': (filename, open(filename, 'rb'))}
   response = requests.post(url, cookies=cookies, files=files, timeout=10, verify=True)
   # check to see if it said file already exists "already exists" or didn't work "not uploaded successfully"
   soup=BeautifulSoup(response.text, "lxml")
   for script in soup(["script", "style"]):
      script.decompose()
   stripped_text=soup.get_text()
   print(stripped_text)
   if 'already exists' in stripped_text:
      print("Existing file named", filename)
      raise ValueError("Existing file named"+filename)
   if 'not uploaded successfully' in stripped_text:
      print("Did not upload successfully")
      raise ValueError("Did not upload successfully")
   if 'not authorized' in stripped_text:
      print("Not authorized to submit updates")
      raise ValueError("Not authorized by ExoFOP")
   print(stripped_text[stripped_text.find('Bulk'):].replace(':', ':\n').replace('\n\n', '\n'))
   return stripped_text[stripped_text.find('Bulk'):].replace(':', ':\n').replace('\n\n', '\n')

def update_disposition(url, cookies, tid, tfopdisp, notes, ctoi=None, toi=None):
   if toi and ctoi:
      print("can't have both toi and ctoi fields")
      return
   if toi:
      files = {
          'toi': (None, toi),
          'tid': (None, tid),
          'tfopdisp': (None, tfopdisp),
          'notes': (None, notes),
      }
   if ctoi:
      files = {
          'ctoi': (None, ctoi),
          'tid': (None, tid),
          'tfopdisp': (None, tfopdisp),
          'notes': (None, notes),
      }
   response = requests.post(url, cookies=cookies, files = files)
   soup=BeautifulSoup(response.text, "lxml")
   for script in soup(["script", "style"]):
      script.decompose()
   stripped_text=soup.get_text()
   if 'Sorry' in stripped_text:
      print("something went wrong on ", tid)
      print(stripped_text)
   return response

if __name__ == "__main__":
   pass

