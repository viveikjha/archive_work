from pylab import *
from astropy.io import fits
import shutil
data=np.genfromtxt('rename_again2.dat',dtype=str)

for i in range(0,len(data)):
    try:
        name=data[i]
        #image=fits.open(name)
        #header=image[0].header
        #print(name,'kinetic mode:',header['NAXIS3'])
        shutil.move(name, '/data/archived_data/processed_data/DFOT/2019A/not_renamed2/')

    except FileNotFoundError:
        print(name)