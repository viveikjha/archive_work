import glob
from astropy.io import fits
import os

path=os.getcwd()
folder=path+'/20211025/'
files=sorted(glob.glob(folder+'*fits'))


for i in range(len(files)):
    name=files[i]
    col1=os.path.basename(name)
   
    if ('bias' in col1):
        col2='BIAS'
        filter='FREE'
        print(col1,col2,filter)
    elif ('flat' in col1):
        col2='FLAT'

    if( '_U' in col1):
        filter='U'
        col2= col1.partition('_')[0]
        print(col1,col2,filter)
    
    elif('_B' in col1):
        filter='B'
        col2= col1.partition('_B')[0]
        print(col1,col2,filter)

    elif('_V' in col1):
        filter='V'
        col2= col1.partition('_V')[0]
        print(col1,col2,filter)

    elif('_R' in col1):
        filter='R'
        col2= col1.partition('_R')[0]
        print(col1,col2,filter)

    elif('_I' in col1):
        filter='I'
        col2= col1.partition('_I')[0]
        print(col1,col2,filter)

    else:
        filter='FREE'
        col2= col1.partition('_')[0]
        print(col1,col2,filter)