import glob
from astropy.io import fits
path='/data/final_data/2016/Nov/DFOT/2K_IMG1/20161119/'

files=sorted(glob.glob(path+'*.fits'))
print(len(files))

for i in range (0,len(files)):
    test_fits=fits.open(files[i])
    test_head=test_fits[0].header
    print(test_head)
