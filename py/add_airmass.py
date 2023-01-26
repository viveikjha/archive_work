import glob
from astropy.io import fits
import os
import shutil
from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle
from astropy import units as u 
import numpy as np


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
            with fits.open(name, mode = 'update',output_verify='fix') as data:
                try:
                    header=data[0].header
                    ra=header['RA']
                    dec=header['DEC']
                    filters=header['FILTER1']
                    airmass=header['AIRMASS']
                    category=header['CATEGORY']
                    instrument=header['INSTRUME']
                    if (instrument=='2K_IMG1'):
                        if (category=='Science'):
                            if (ra=='NULL'):
                                print(col1,'Null RA value!')
                            else:
                                ra=float(ra)
                                dec=float(dec)
                                lon= header['GEOLONG']
                                lat= header['GEOLAT']
                                c = SkyCoord(lon, lat, frame = 'icrs', unit = 'deg')
                                lon = c.ra.value
                                lat = c.dec.value
                                lst= header['LST']
                                LST = Angle(lst + ' hours').deg
                                LST=float(LST)
                                # Alt & Az calculated based on equations of http://www.stargazing.net/kepler/altaz.html
                                # Also see the calculator: http://jukaukor.mbnet.fi/star_altitude.html
                                #print(LST,ra)
                                ha = LST - ra
                                if ha < 0.0: ha = ha + 360
                                sin_dec = np.sin(np.radians(dec))
                                sin_lat = np.sin(np.radians(lat))
                                cos_lat = np.cos(np.radians(lat))
                                cos_dec = np.cos(np.radians(dec))
                                # Alt:
                                alt0 = sin_dec * sin_lat + cos_dec * cos_lat * np.cos(np.radians(ha))
                                alt1 = np.arcsin(alt0)     #in radians
                                alt  = np.degrees(alt1)    #in degrees
                                sin_alt = alt0
                                cos_alt = np.cos(np.radians(alt))
                                #Az:
                                az0 = np.arccos( (sin_dec - sin_alt*sin_lat) / (cos_alt*cos_lat ) )
                                if np.sin(np.radians(ha))<0: az = np.degrees(az0)
                                else: az = 360 - np.degrees(az0)
                                airmass = 1 / np.cos(np.radians(90 - alt)) 
                                alt_angle = Angle(alt, u.deg).to_string(unit = u.degree, sep=':')
                                az_angle = Angle(az, u.deg).to_string(unit = u.degree, sep=':')
                                header['ALTITUDE'] = str(alt_angle)
                                header['AZIMUTH']  = str(az_angle)
                                header['AIRMASS']  = airmass
                                print(col1,airmass,'airmass updated')

        



                except OSError:
                    print(name,'Corrupt file')
                    continue
                except KeyError:
                    print(name,'\t','astrometry failed')
                
                

                continue

