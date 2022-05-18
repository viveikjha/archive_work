"""
Created on Thur Oct-29-2020

@author: Sapna Mishra

Use to perform the astrometry from solve-field task
"""

from __future__ import print_function, division
import time
import subprocess
import glob, os, fnmatch, timeit
import numpy as np
from matplotlib import pylab as plt
from scipy import stats
import matplotlib, sys
import numpy.ma as ma
import sep
from astropy.io import fits
from astropy import wcs
import astropy.units as u
from astropy.coordinates import SkyCoord
import ephem
import warnings
warnings.filterwarnings("ignore")
#################
gatech = ephem.Observer()
gatech.lon, gatech.lat = '+79.6841', '+29.3612'
gatech.elevation = 2450.0

def get_LST(ddd):
    date_ut = ddd.split('T',2)
    ddd = date_ut[0]; date=ddd.replace('-','/',3)
    ddd = date_ut[1]; ut = ddd.split(':',2)   
    ut_deg =  float(ut[0]) + float(ut[1])/60.0 + float(ut[2])/3600.0
    gatech.date = date+' '+str(ut_deg) 
    LST_hms = str(gatech.sidereal_time()).split(':',2)   
    #LST_deg = ( float(LST_hms[0])*1.0 + float(LST_hms[1])/60.0 + float(LST_hms[2])/3600.0) * 360.0/ 24.0
    LST_p = ( (float(LST_hms[0])*1.0+4.0) + float(LST_hms[1])/60.0 + float(LST_hms[2])/3600.0) * 360.0/ 24.0
    LST_n = ( (float(LST_hms[0])*1.0 -4.0 )+ float(LST_hms[1])/60.0 + float(LST_hms[2])/3600.0) * 360.0/ 24.0
    print(LST_p,LST_n)
    return LST_deg
###################################

## FOV: DOT:6.5 x 6.52 arcmin, ST: 6.81 x 7.02 arcmin, DFOT: 18.5 x 18.5 arcmin
pwd = os.getcwd()

telescope_tag = str(input("Enter the telescope (DFOT: df, ST: s, DOT: d) : "))


class init_data:
    def __init__(self,telescope,pixscale_err,percent_error,index_ver_arr):
        self.telescope=telescope
        self.pixscale_err=pixscale_err
        self.percent=percent_arr
        self.index_ver_arr=index_ver_arr


    def description(self):
        return f"{self.telescope} pixel scale is {self.pix} ."

    def test_object(self):
        return f"This is a test object for {self.telescope}."

df=init_data("DFOT",0.5354,0.02)
print(df.telescope)




def init_process():
    dir_data     = ['/DFOT','/ST', '/DOT']
    pixscale_arr = [0.535495973, 0.314,0.191]
    percent_arr  = [0.02, 0.02, 0.02]
    index_ver_arr = ['4100','4200','5000']
    
    if telescope_tag == "df":
        os.chdir(pwd+dir_data[0])
        pixscale = pixscale_arr[0]
        percent = percent_arr[0]
        index_ver = index_ver_arr[1]

    if telescope_tag == "s":
        os.chdir(pwd+dir_data[1])
        pixscale = pixscale_arr[1]
        percent = percent_arr[1]
        index_ver = index_ver_arr[2]

    if telescope_tag == "d":
        os.chdir(pwd+dir_data[2])
        pixscale = pixscale_arr[2]
        percent = percent_arr[2]
        index_ver = index_ver_arr[2]
        
    return pixscale,percent,index_ver


pixscale,percent, index_ver=  init_process()

f = 0
start = timeit.default_timer()
for file in glob.glob("*.fits"):
    image, header = fits.getdata(file, ext=0,header=True)
    #date_obs = header['DATE-OBS']
    #LST = get_LST(date_obs)          ### Give time in UT
    #RA0,DEC0  = header['CRVAL1'], header['CRVAL2']
    #RA_str, DEC_str = str(RA0), str(DEC0)
    
    pixscale_l,pixscale_u = str(pixscale - (pixscale*percent)), str(pixscale + (pixscale*percent))
    os.system('solve-field --continue --downsample 2 --no-plots --scale-low '+pixscale_l+' --scale-high '+pixscale_u+' --scale-units app --config /home/aries/Divyansh/cfg '+file)
    #os.system('solve-field --continue --downsample 2 --no-plots --scale-low '+pixscale_l+' --scale-high '+pixscale_u+' --scale-units app --config /home/aries/Divyansh/cfg --ra '+RA_str+' --dec '+DEC_str+' --radius 10 '+file)
    
    f = f + 1
    
end = timeit.default_timer()
print('Astrometry finished in : '+str(np.round(end-start))+'s  for '+str(f)+' files')
