
import glob
from astropy.io import fits
import os
import shutil

root=os.getcwd()
#folder=path+'/20220201/'
#files=sorted(glob.glob(folder+'*fits'))

#print("FileName","\t","Object","\t","Filter")
for path, subdirs, files in os.walk(root):
    for file_name in files:
        name=os.path.join(path, file_name)
        col1=os.path.basename(name)
        
    
        if ('fits' in col1):
            
            #info=data[0].data
            try:
                print(name)
            except OSError:
                print(name,'Corrupt file')
            
            
            


