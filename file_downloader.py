#!/usr/bin/env python3
import pandas as pd
import requests
from bs4 import BeautifulSoup
from os import listdir
import io

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

def file_get_new(TIC):
   TIC_url="https://exofop.ipac.caltech.edu/tess/download_filelist.php?id="+str(TIC)
   test=requests.get(TIC_url)
   return pd.read_csv(io.StringIO(test.text), sep='|')

def file_download(file_name, file_ID, download_counter):
   print("Downloading ", file_name)
   url="https://exofop.ipac.caltech.edu/tess/get_file.php?id="+str(file_ID)
   #print(url); quit()
   r=requests.get(url, allow_redirects=True)
   destination_file=file_dir+"/"+file_name
   open(destination_file, 'wb').write(r.content)
   return download_counter+1


def bulk_download(obs_type, file_dir=".", user=None, file_substring=[".tbl"], file_search_dict={}, file_ext=None):
   for item in file_search_dict:
      file_search_dict[item]=file_search_dict[item].split('|')
   print(file_search_dict)
   #quit()
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

   already_downloaded=0
   downloads=0
   download_list=[]
   for TIC in observed_TIC_list:
      #TIC_table=file_get(TIC)
      #if verbose: print(test)
      #if verbose: print(test['url'].values)
      #if verbose: print(TIC_table)
      #TIC=269558487
      ####TIC_url="https://exofop.ipac.caltech.edu/tess/download_filelist.php?id="+str(TIC)
      ####test=requests.get(TIC_url)
      #if verbose: print(test)
      #if verbose: print(test.text)
      #test_df=pd.read_csv(test.text, sep='|')
      #test_df=pd.read_csv(io.StringIO(test.text), sep='|')
      test_df=file_get_new(TIC)
      for item in file_search_dict:
         for value in file_search_dict[item]:
            test_df=test_df[test_df[item].str.contains(value)]
      if verbose: print(test_df)
      #quit()
      #print(test_df['File Name'])
      if verbose: print("File extention: ", file_ext)
      if file_ext:
            test_df=test_df[test_df['File Name'].str.endswith(file_ext)]
      if verbose: print(test_df)
      #quit()
      #df=df[df['url'].str.contains("get_file")]
      #if verbose: print(test_df.iloc[0])
      for index, row in test_df.iterrows():
         if row['File Name'] in existing_files:
            print("Have downloaded %s" % row['File Name'])
            already_downloaded=already_downloaded+1
         else:
            print("Don't have %s" % row['File Name'])
            if verbose: print(row)
            download_list.append({'file name': row['File Name'], 'file ID': row['File ID']})
   print(download_list)
   print("Already downloaded: ", already_downloaded)
   print(len(download_list), " files to download")
   #quit()
   for item in download_list:
      print(item)
      #print(item[0])
      downloads=file_download(item['file name'], item['file ID'], downloads)
   #quit()
   #   quit()
   #   for index, row in TIC_table.iterrows():
   #      if row['text'] in existing_files:
   #         print("Already downloaded %s" % row['text'])
   #      else:
   #         print("Downloading %s" % row['text'])
   #         url="https://exofop.ipac.caltech.edu/tess/"+row['url']
   #         print(url); quit()
   #         r=requests.get(url, allow_redirects=True)
   #         destination_file=file_dir+"/"+row['text']
   #         open(destination_file, 'wb').write(r.content)
   #         downloads+=1
   print("%.0f files downloaded" % downloads)


if __name__ == '__main__':
   verbose=False
   #verbose=True
   obs_type="Imaging" #Imaging, Spectroscopy, Time Series
   file_dir="ExoFOP_data" #location to save files and check for previous files
   user="ciardi" # user that has uploaded the files being searched for
   file_substring=[".tbl", "-dc"] # substrings to search for in filenames
   #Type, File Name, TIC (not recommended), TOI (not recommended), Date, User, Group, Tag (number only), Description 
   file_search_dict={"User":"ciardi", "File Name": ".tbl|-dc"}
   file_search_dict={"User":"ciardi", "File Name": ".tbl"}
   file_search_dict={"User":"ciardi", "File Name": ".fits"}
   file_search_dict={"User":"ciardi", "File Name": "TOI|_plot", "Type":"Image"}
   file_ext=".fits"
   file_substring=["_plot", "-dc"] # substrings to search for in filenames
   file_ext=".jpg"
   #print(search_dict)
   #quit()
   bulk_download(obs_type, file_dir, user=user, file_substring=file_substring, file_search_dict=file_search_dict, file_ext=file_ext)
