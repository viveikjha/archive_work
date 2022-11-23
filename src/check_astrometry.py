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
                category=header['CATEGORY']
                orig=header['ORIGFILE']
                if (category=='Science'):
                    if (ra=='NULL'):
                        print(name,filters,'\t','astrometry Failed')
                        shutil.move(name, '/data/archived_data/processed_data/DFOT/failed_2019A/')
                        print('\n file without astrometry moved \n ')
                    else:
                        print(name,ra,dec,filters, '\t','astrometry successful')
                if (category=='Calibration'):
                    print(name,'calibration file only!')
            except OSError:
                print(name,'Corrupt file')
                shutil.move(name, '/data/archived_data/processed_data/DFOT/failed_2019A/')

                continue
            except KeyError:
                print(name,'\t','astrometry failed')
                shutil.move(name, '/data/archived_data/processed_data/DFOT/failed_2019A/')

            

            continue

