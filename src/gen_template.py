import glob
from astropy.io import fits
import os

root=os.getcwd()
#folder=path+'/20220201/'
#files=sorted(glob.glob(folder+'*fits'))

print("FileName","\t","Object","\t","Filter1")
for path, subdirs, files in os.walk(root):
    for file_name in files:
        if ('fits' in file_name):
            name=os.path.join(path, file_name)
            col1=os.path.basename(name)
        
            if ('bias' in col1):
                col2='BIAS'
                filter='FREE'
                
                print(col1,"\t",col2,"\t",filter)
            elif ('flat' in col1):
                col2='FLAT'

            if( '_u' in col1 or '_U' in col1):
                filter='U'
                col2= col1.partition('_')[0]
                print(col1,"\t",col2,"\t",filter)
            
            elif('_b' in col1 or '_B' in col1):
                filter='B'
                col2= col1.partition('_')[0]
                print(col1,"\t",col2,"\t",filter)

            elif('_v' in col1 or '_V' in col1):
                filter='V'
                col2= col1.partition('_')[0]
                print(col1,"\t",col2,"\t",filter)

            elif('_r' in col1 or '_R' in col1):
                filter='R'
                col2= col1.partition('_')[0]
                print(col1,"\t",col2,"\t",filter)

            elif('_i' in col1 or '_I' in col1):
                filter='I'
                col2= col1.partition('_')[0]
                print(col1,"\t",col2,"\t",filter)

            elif('_Ha' in col1):
                filter='Ha'
                col2= col1.partition('_')[0]
                print(col1,"\t",col2,"\t",filter)

            elif('_OIII' in col1):
                filter='OIII'
                col2= col1.partition('_')[0]
                print(col1,"\t",col2,"\t",filter)

            else:
                filter='FREE'
                col2= col1.partition('_')[0]
                print(col1,"\t",col2,"\t",filter)


# If people are using sdss ugriz filter, please let us know in advance? Stuck with this for the time being.
