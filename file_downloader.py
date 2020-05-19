#!/usr/bin/env python3
import pandas as pd
import requests
from bs4 import BeautifulSoup
from os import listdir

# Allows for large-scale downloading of files with predictable file names
# Currently uses the imaging table to get the list of TOIs to check for files

#get tbl files for a TOI
def file_get(TIC):
   url = "https://exofop.ipac.caltech.edu/tess/target.php?id="+str(TIC)
   page = requests.get(url)
   data= page.text
   soup = BeautifulSoup(data, 'html.parser')
   x=[[link.get('href'), link.get_text()] for link in soup.find_all('a')]
   df = pd.DataFrame(x, columns = ['url', 'text']) 
   df=df.dropna(how='any')
   df=df[df['url'].str.contains("get_file")]
   for substring_1 in file_substring:
      df=df[df['text'].str.contains(substring_1)]
   return df

def bulk_download(obs_type, file_dir=".", user=None, file_substring=[".tbl"]):
   existing_files=listdir(file_dir)
   page_term=None
   if obs_type.lower()[0]=="i": page_term="imaging"
   if obs_type.lower()[0]=="s": page_term="spect"
   if obs_type.lower()[0]=="t": page_term="tseries"
   if not page_term:
      print("Not a valid category of observations")
      quit()
   source_file="https://exofop.ipac.caltech.edu/tess/download_"+page_term+".php?sort=id&output=pipe"
   print(source_file)
   obs_df=pd.read_csv(source_file, sep='|')
   if user:
      obs_df=obs_df[obs_df['User'].str.contains(user)]
   if verbose: print(obs_df)
   observed_TOIs=obs_df['TIC ID'].values
   observed_TIC_list=list(dict.fromkeys(observed_TOIs))
   if verbose: print(observed_TIC_list, len(observed_TIC_list))
   print("%.0f TOIs observed" % len(observed_TIC_list))


   downloads=0
   for TIC in observed_TIC_list:
      TIC_table=file_get(TIC)
      if verbose: print(test)
      if verbose: print(test['url'].values)
      for index, row in TIC_table.iterrows():
         if row['text'] in existing_files:
            print("Already downloaded %s" % row['text'])
         else:
            print("Downloading %s" % row['text'])
            url="https://exofop.ipac.caltech.edu/tess/"+row['url']
            r=requests.get(url, allow_redirects=True)
            destination_file=file_dir+"/"+row['text']
            open(destination_file, 'wb').write(r.content)
            downloads+=1
   print("%.0f files downloaded" % downloads)


if __name__ == '__main__':
   verbose=False
   obs_type="Imaging" #Imaging, Spectroscopy, Time Series
   file_dir="ExoFOP_data" #location to save files and check for previous files
   user="ciardi" # user that has uploaded the files being searched for
   file_substring=[".tbl", "-dc"] # substrings to search for in filenames
   bulk_download(obs_type, file_dir, user=user, file_substring=file_substring)
