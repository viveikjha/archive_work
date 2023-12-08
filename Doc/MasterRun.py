import os 
import easygui as eg
import numpy as np
import shutil

doc_files = '/data/archived_data/processed_data/DFOT/2022B/src/Doc/'
lst_dir = np.loadtxt(doc_files+'dir_lst.txt',usecols=[0],unpack=True,dtype='str')

try:
    for ff in range(0,len(lst_dir)):
        os.chdir(lst_dir[ff])
        os.system('python3  '+doc_files+'AppendHeaderNew.py')
except TypeError:
    os.system('python3  '+doc_files+'AppendHeaderNew.py')
