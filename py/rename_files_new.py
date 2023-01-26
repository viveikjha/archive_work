import glob
from astropy.io import fits
import os
def check_extension(fname,ext):  
    return fname.endswith(ext)  


count = 0
root=os.getcwd()
for path, subdirs, files in os.walk(root):
    for name in files:
        file_name=os.path.join(path, name)
        if check_extension(file_name,'dat'):  
            os.remove(os.path.join(path,file_name))


       
        if 'fits' in file_name and 'S-' in file_name:  ## Here we check whether the files are bias/flat/science.
            data=fits.open(file_name)
            #print(file_name)
            #count+=1
            header=data[0].header
            date_obs =header['DATE-OBS']
            mod_date=date_obs[0:10].replace('-','')  # Here we put a condition for dividing the data into cycles.
            mod_date=int(mod_date)
          
            telescope = header['TELESCOP']
            instrument = header['INSTRUME']
            category=header['CATEGORY']
           
            if mod_date >20160331 and mod_date < 20160701: # The if condition in order to divide the data into cycles.
                count+=1
                code='S'
                cycle='2016B'
                text='PXX' # This tex has to be specific to DFOT. analogous to proposal ID.
                #print(count,code,cycle,text,date_obs,telescope,instrument,category)
                #print(count,code+'-'+cycle+'-'+text+'-'+date_obs+'-'+telescope+'-'+instrument+'.fits')
                #print(file_name)
                os.rename(file_name,os.path.join(path,code+'-'+cycle+'-'+text+'-'+date_obs+'-'+telescope+'-'+instrument+'.fits'))
                print(count,'done!!')
      
