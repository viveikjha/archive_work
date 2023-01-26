import glob
from astropy.io import fits
import os

count = 0
root=os.getcwd()
for path, subdirs, files in os.walk(root):
    for name in files:
        file_name=os.path.join(path, name)
        if 'fits' in file_name:
            data=fits.open(file_name)
            count+=1
            header=data[0].header
            date_obs =header['DATE-OBS']
            telescope = header['TELESCOP']
            instrument = header['INSTRUME']
            category=header['CATEGORY']
            print(count,date_obs,telescope,instrument,category)

'''
for iname in glob.glob("*.fits"):
  with fits.open(iname) as hdul:
    obj = hdul[0].header['OBJECT']
    date_obs = hdul[0].header['DATE-OBS']
    #date = date_obs.replace(".","_")
    telescope = hdul[0].header['TELESCOP']
    instru = hdul[0].header['INSTRUME']


    if (obj == 'flat' or obj == 'FLAT' or obj == 'Flat'):
      code = 'F'
    elif (obj == 'bias' or obj == 'BIAS' or obj == 'Bias'):
      code = 'B'
    elif (obj == 'test' or obj == 'TEST' or obj == 'Test'):
      code = 'T'
    else:
      code = 'S'

    #print(iname,code,obj,date_obs,telescope,instru)
    if os.path.isfile(code+'-2020C2P74-'+date_obs+'-'+telescope+'-'+instru+'.fits') == False:
      os.rename(iname,code+'-2020C2P74-'+date_obs+'-'+telescope+'-'+instru+'.fits')
    else:
      os.rename(iname,code+'-2020C2P74-'+date_obs+'-'+telescope+'-'+instru+f'{counter}'+'.fits')
    counter = counter + 1

'''