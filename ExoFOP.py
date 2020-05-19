#!/usr/bin/python3

#load the parameters stored in local file of following format:
#username=[username]
#password=[password]
#url=https://exofop.ipac.caltech.edu/tess/password_check.php
#status='' This value is used for internal testing and can be ignored or excluded

def ExoFOP_parameters(file_name):
   params={}
   params['status']=''
   with open(file_name) as fp:
      for line in fp:
         line=line.strip()
         items=line.split('=')
         params[items[0]]=items[1]
   params['cookie']='exocookies_'+params['username']+params['status']+'.txt'
   return params

def get_private_table(table_url, params):
   response=requests.get(url, cookies=params['cookie'])
   soup=BeautifulSoup(response.text, "lxml")
   for script in soup(["script", "style"]):
      script.decompose()
   stripped_text=soup.get_text()
   TESTDATA=StringIO(stripped_text)
   df_csv=pd.read_csv(TESTDATA, index_col=0, delimiter=",",  warn_bad_lines=True)#, error_bad_lines=False)#, usecols=['ID', 'TIC ID', 'Username', 'TAG ID', 'notes'])
   return df_csv


if __name__ == '__main__':
   import sys
   params=ExoFOP_parameters(sys.argv[1])
   print(params)
   print(get_private_table(table_url, params))
