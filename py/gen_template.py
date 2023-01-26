import glob
from astropy.io import fits
import os

root=os.getcwd()
#folder=path+'/20220201/'
#files=sorted(glob.glob(folder+'*fits'))

print("FileName","\t","Object","\t","Filter")
for path, subdirs, files in os.walk(root):
    for file_name in files:
        name=os.path.join(path, file_name)
        col1=os.path.basename(name)
    
        if ('bias' in col1):
            col2='BIAS'
            filter='FREE'
            
            print(name,"\t",col2,"\t",filter)
        elif ('flat' in col1):
            col2='FLAT'

        if( '_U' in col1):
            filter='U'
            col2= col1.partition('_')[0]
            print(name,"\t",col2,"\t",filter)
        
        elif('_B' in col1):
            filter='B'
            col2= col1.partition('_')[0]
            print(name,"\t",col2,"\t",filter)

        elif('_V' in col1):
            filter='V'
            col2= col1.partition('_')[0]
            print(name,"\t",col2,"\t",filter)

        elif('_R' in col1):
            filter='R'
            col2= col1.partition('_')[0]
            print(name,"\t",col2,"\t",filter)

        elif('_I' in col1):
            filter='I'
            col2= col1.partition('_')[0]
            print(name,"\t",col2,"\t",filter)

        elif('_Ha' in col1):
            filter='Ha'
            col2= col1.partition('_')[0]
            print(name,"\t",col2,"\t",filter)

        else:
            filter='FREE'
            col2= col1.partition('_')[0]
            print(name,"\t",col2,"\t",filter)