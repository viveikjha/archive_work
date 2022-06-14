import glob
from astropy.io import fits
import os
def check_extension(fname,ext):  
    return fname.endswith(ext)  


count = 0
root= '/data/archived_data/final_data/2016/Dec/'
for path, subdirs, files in os.walk(root):
    for name in files:
        file_name=os.path.join(path, name)
        if check_extension(file_name,'dat'):  
            os.remove(os.path.join(path,file_name))


       
        if 'fits' in file_name :  ## Here we check whether the files are bias/flat/science.
            data=fits.open(file_name)
            print(file_name)
            image=data[0].data
            header=data[0].header
            filt=header['FILTER']
            #print(filt)
            header.set('FILTER1',filt,after='GRISM')
            header.set('FILTER2',None,after='FILTER1')
            del header['FILTER']
            fits.writeto(file_name,image,header=header,overwrite=True)
            count+=1
            print(count,'done!!')
      