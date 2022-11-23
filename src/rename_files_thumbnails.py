import glob
from astropy.io import fits
import os
import shutil
import aplpy
import warnings

warnings.filterwarnings('ignore')


root=os.getcwd()


for path, subdirs, files in os.walk(root,topdown=False):
    count=0
    thumb_folder='thumbnails'
    thumb_path=os.path.join(path,thumb_folder)

    if os.path.exists(thumb_path):
        shutil.rmtree(thumb_path)
    os.mkdir(thumb_path)

    for file_name in files:
        name=os.path.join(path, file_name)
        col1=os.path.basename(name)
        dir_path=os.path.dirname(name)  
    


        if ('fits' in col1):
            data=fits.open(name)
            header=data[0].header
            #image=data[0].data
            obj = header['OBJECT']
            date_obs = header['DATE-OBS']
            telescope = header['TELESCOP']
            instru = header['INSTRUME']
            if (obj == 'flat' or obj == 'FLAT' or obj == 'Flat'):
                code = 'F'
            elif (obj == 'bias' or obj == 'BIAS' or obj == 'Bias'):
                code = 'B'
            elif (obj == 'test' or obj == 'TEST' or obj == 'Test'):
                code = 'T' 
            else:
                code = 'S'
            new_name=code+'-2022BPXX-'+date_obs+'-'+telescope+'-'+instru+'.fits'
           
            #print(header.keys())

            (prefix, sep, suffix) = new_name.rpartition('.')
            thumb_name=prefix
           # print(thumb_path+'/{}.png'.format(thumb_name))

            if ('CRVAL1' in header.keys()):
                print(col1,'astrometry done')
                try:
                    f1=aplpy.FITSFigure(name)
                    f1.show_grayscale()
                    f1.axis_labels.set_xtext('RA (J2000)')
                    f1.axis_labels.set_ytext('Dec (J2000)')
                    f1.save(thumb_path+'/{}.jpg'.format(thumb_name),dpi=60)
                    print('Thumbnail saved!!')
      
                except KeyError:
                    print("Keyword issue!")
                    continue
                except TypeError:
                    print ("Kinetic mode image..no thumbnail generated!!!")
                    continue
            
                    
            print(count,':processed')
            os.rename(name,os.path.join(path,new_name))
            count+=1
             
    if not os.listdir(root[0]):
        os.remove(dirs(root[0]))
 
