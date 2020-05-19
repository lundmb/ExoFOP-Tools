#!/usr/bin/python3
import numpy as np
import sys
import pandas as pd
table_url='https://exofop.ipac.caltech.edu/tess/download_toi.php?sort=toi&output=pipe'


def TOI_lookup(TIC_ID): # Get list of TOIs given TIC ID
   TOI_table=pd.read_csv('https://exofop.ipac.caltech.edu/tess/download_toi.php?sort=toi&output=pipe', delimiter='|')
   TOI_table=TOI_table.loc[TOI_table['TIC ID'] == TIC_ID]
   return TOI_table['TOI'].values

def TIC_lookup(TOI): # Get TIC ID given TOI (planet does not need to be specified, either 101 or 101.01 will work)
   TOI_table=pd.read_csv('https://exofop.ipac.caltech.edu/tess/download_toi.php?sort=toi&output=pipe', delimiter='|')
   if int(TOI)==TOI:
      TOI=TOI+.01
   TOI_table=TOI_table.loc[TOI_table['TOI'] == TOI]
   return TOI_table['TIC ID'].values


if __name__ == '__main__':
   # Run functions from command line:
   # For fetching TOIs:
   # python3 TOI_lookup.py getTOI 278683844
   # For fetching TIC ID:
   # python3 TOI_lookup.py getTIC 101.01
   # or
   # python3 TOI_lookup.py getTIC 101

   if sys.argv[1] == 'getTOI':
      print(TOI_lookup(int(sys.argv[2])))
   if sys.argv[1] == 'getTIC':
      print(TIC_lookup(float(sys.argv[2])))

