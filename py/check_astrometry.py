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
                data=fits.open(name)
                header=data[0].header
                ra,dec=header['RA'],header['DEC']
                filters=header['FILTER1']
                airmass=header['AIRMASS']
                category=header['CATEGORY']
                instrument=header['INSTRUME']
                if (instrument=='2K_IMG1'):
                    if (ra=='NULL'):
                        print(col1,ra,dec,airmass,'\t','astrometry Failed')
                        #shutil.move(name, '/data/archived_data/processed_data/DFOT/failed_astrometry_2020A/')
                        #print('\n file without astrometry moved \n ')
                    if (category=='Calibration'):
                        print(col1,'calibration file only!')
                    else:
                        print(col1,ra,dec,airmass, '\t','astrometry successful')


    



            except OSError:
                print(name,'Corrupt file')
                continue
            except KeyError:
                print(name,'\t','astrometry failed')
            
            

            continue

