import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle
from astropy import units as u
import glob 

files=glob.glob("*.fits*")
#files = ['/data/archived_data/processed_data/ST/Imaging/2020/Apr2020/20200420/2020ftl_r_1024x1024_8.fits']
file1 = open("airmass_new.txt", "w")
all_airmass= np.array([])
for i in range(len(files)):
    with fits.open(files[i], mode = 'update',output_verify='fix') as hdu:
        try:
            print(i, files[i])
            ra = float(hdu[0].header['RA'])
            dec= float(hdu[0].header['DEC'])
            lon= hdu[0].header['GEOLONG']
            lat= hdu[0].header['GEOLAT']
            c = SkyCoord(lon, lat, frame = 'icrs', unit = 'deg')
            lon = c.ra.value
            lat = c.dec.value
            lst= hdu[0].header['LST']
            LST = Angle(lst + ' hours').deg
            # Alt & Az calculated based on equations of http://www.stargazing.net/kepler/altaz.html
            # Also see the calculator: http://jukaukor.mbnet.fi/star_altitude.html
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
            header = hdu[0].header
            data = hdu[0].data
            alt_angle = Angle(alt, u.deg).to_string(unit = u.degree, sep=':')
            az_angle = Angle(az, u.deg).to_string(unit = u.degree, sep=':')
            header['ALTITUDE'] = str(alt_angle)
            header['AZIMUTH']  = str(az_angle)
            header['AIRMASS']  = airmass
            print("ha, airmass, alt, az:", ha, airmass, alt, az)
            file1.write('{0}\t {1}\n'.format(files[i], airmass))
        except: pass
file1.close()

#plt.figure()
#plt.hist(all_airmass)
#plt.xlabel("AIRMASS")
#plt.savefig("airmass.pdf", bbox_inches='tight')
#plt.close()
