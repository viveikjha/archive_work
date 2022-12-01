import numpy as np
from ztfquery import lightcurve
import csv
ra,dec=np.genfromtxt("ra_dec_spiders_agn.dat",unpack=True,usecols=(0,1))
username=input('Enter Username for IRSA:\t')
password=input('Enter Password for IRSA:\t')
count=0

for i in range(0,len(ra)):
    print(ra[i],dec[i])
    data = lightcurve.LCQuery.download_data(circle=[ra[i],dec[i],0.0014], bandname="g",auth=[username,password])
    date_init=data['mjd']
    mag_init=data['mag']
    magerr_init=data['magerr']
    catflag=data['catflags']
    ra_init=data['ra']
    dec_init=data['dec']
    #good_id = np.where(catflag == 0)[0]
    #date,mag,magerr,ra,dec= date[good_id],mag[good_id],magerr[good_id],ra[good_id],dec[good_id]
    #Date.append(date)
    #Mag.append(mag)
    #Mag_Err.append(magerr)
    #RA.append(ra)
    #DEC.append(dec)

    if len(date_init)==0:
        print('file has no data points')
        count+=1
    elif len(date_init)<=100:
        print('less than 100 data points')
        count+=1
    else:
        with open("spiders_lc_reduced/{}_{}.g.csv".format(ra[i],dec[i]), 'w+') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(zip(date_init,mag_init,magerr_init))
            print("Light curve no {} downloaded.".format(i+1))

print(count)
