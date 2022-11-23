#!/usr/bin/env python
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #
# xxxxxxxxxxxxxxxxxxxxxxx----------------Append Observatory Details To The Header-------------xxxxxxxxxxxxxxxxxxxxxxx #
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #

# ------------------------------------------------------------------------------------------------------------------- #
# Import Required Libraries
# ------------------------------------------------------------------------------------------------------------------- #
import os
import re
import sys
import glob
import ephem
import subprocess
import numpy as np
import pandas as pd
import easygui as eg
from datetime import datetime, timedelta
from astropy import units as u
from astropy import wcs
from astropy.io import fits
from astropy.coordinates import Angle, SkyCoord
import aplpy
import shutil
# ------------------------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------------------------- #
# Files to be Read
# ------------------------------------------------------------------------------------------------------------------- #
DIR_DOC = '/data/archived_data/processed_data/DFOT/2022B/src/Doc/'
file_telescopes = DIR_DOC+'TelescopeList.csv'
file_instruments = DIR_DOC+'InstrumentList.csv'
file_keywords = DIR_DOC+'MasterHeaderList.dat'
file_template = 'TemplateFileList.dat'

# Telescope and Instrument Details
telescope_df = pd.read_csv(file_telescopes, sep=',', comment='#').set_index('ShortName')
instrument_df = pd.read_csv(file_instruments, sep=',', comment='#').set_index('ShortName')

# Read the Master-List of Header Keywords
# Read the File containing OBJECT and FILTER keyword details
keywords_df = pd.read_csv(file_keywords, sep='\s+', comment='#').set_index('Header')
keywords_df = keywords_df.fillna('NULL')
header_df = pd.read_csv(file_template, sep='\s+', comment='#', dtype='string').set_index('FileName')

#header_df = pd.read_csv(file_template, sep='\s+', comment='#', dtype='string').set_index('Object') # neha
# ------------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------------------------- #
# Image Header Keywords [Required for Airmass Computation and Appending Header Details]
# ------------------------------------------------------------------------------------------------------------------- #
EXPOSURE_keyword = 'EXPTIME'
DATE_keyword = 'DATE-OBS'
RA_keyword = 'RA'
DEC_keyword = 'DEC'
UT_keyword = 'UT'
FILTER_keyword = 'FILTER1'
OBJECT_keyword = 'OBJECT'
# ------------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------------------------- #
# Helper Functions
# ------------------------------------------------------------------------------------------------------------------- #

def group_similar_files(text_list, common_text, exceptions=''):
    """
    Groups similar files based on the string 'common_text'. Writes the similar files
    onto the list 'text_list' (only if this string is not empty) and appends the similar
    files to a list 'python_list'.
    Args:
        text_list   : Name of the output text file with names grouped based on the 'common_text'
        common_text : String containing partial name of the files to be grouped
        exceptions  : String containing the partial name of the files that need to be excluded
    Returns:
        list_files  : Python list containing the names of the grouped files
    """
    list_files = glob.glob(common_text)
    if exceptions != '':
        list_exception = exceptions.split(',')
        for file_name in glob.glob(common_text):
            for text in list_exception:
                test = re.search(text, file_name)
                if test:
                    try:
                        list_files.remove(file_name)
                    except ValueError:
                        pass

    list_files.sort()
    if len(text_list) != 0:
        with open(text_list, 'w') as f:
            for file_name in list_files:
                f.write(file_name + '\n')

    return list_files


def display_text(text_to_display):
    """
    Displays text mentioned in the string 'text_to_display'
    Args:
        text_to_display : Text to be displayed
    Returns:
        None
    """
    print("\n" + "# " + "-" * (12 + len(text_to_display)) + " #")
    print("# " + "-" * 5 + " " + str(text_to_display) + " " + "-" * 5 + " #")
    print("# " + "-" * (12 + len(text_to_display)) + " #" + "\n")

# ------------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------------------------- #
# Functions to help with Identification of ImageType and Instrument
# Functions for Extracting Data, Formatting and Modifying the Date of Observation
# ------------------------------------------------------------------------------------------------------------------- #

def identify_imagetype(filename):
    """
    Append Filter details onto the header of the file 'filename'.
    Args:
        filename : FITS file to which filter details have to be appended.
    Returns:
        True     : When the file is an object
        False    : When the file is a bias or a flat
    """
    with fits.open(filename, mode='update') as hdulist:
        header = hdulist[0].header

        if header[OBJECT_keyword] in ['BIAS', 'FLAT']:
            header['CATEGORY'] = 'Calibration'
            header['TYPE'] = header[OBJECT_keyword]
            return False
        else:
            header['CATEGORY'] = 'Science'
            header['TYPE'] = 'OBJ'
            return True


def identify_instrument(instrument_df, filename):
    """
    Identify the Instrument details using the header of a given file 'filename' in directory to be run.
    Args:
        instrument_df : Pandas DataFrame containing Master-list of Instruments of a specific telescope
        filename      : FITS file from which Instrument details have to be extracted.
    Returns:
        instrument    : Name of the Instrument from which the given file 'filename' was observed.
    """
    with fits.open(filename, mode='update') as hdulist:
        header = hdulist[0].header

        if 'BAXIS1' in header.keys():
            header['XBINNING'] = header['BAXIS1']
            header['YBINNING'] = header['BAXIS2']
        elif 'HBIN' in header.keys():
            header['XBINNING'] = header['HBIN']
            header['YBINNING'] = header['VBIN']

        ysize = int(header['NAXIS1']) * int(header['XBINNING'])
        xsize = int(header['NAXIS2']) * int(header['YBINNING'])

        query = instrument_df[(instrument_df['NAXIS1'] == ysize) & (instrument_df['NAXIS2'] == xsize)]
        instrument = query['Instrument'].values[0]

        return instrument


def extract_extndata(hdulist, extn=0):
    """
    Extracts the data pertaining to a particular extension from a multi-dimensional array stored in a FITS file.
    Args:
        hdulist : HDU which contains the multi-dimensional FITS array
        extn    : Extension number for which the 2-D array is to be extracted
    Returns:
        datanew : 2-D array corresponding to the extension number (extn) specified
    """
    data = hdulist[0].data
    datanew = np.reshape(data[extn, :, :], (data.shape[1], data.shape[2]))
    return datanew


def format_dateobs(dateobs):
    """
    Formats the value of DATE_keyword in the FITS header to account for time in milliseconds.
    Args:
        dateobs : Value of the DATE_keyword that is to be modified
    Returns:
        datenew : Modified value of the DATE_keyword which accounts for time in milliseconds.
    """
    #datetime_master = datetime.strptime(dateobs, '%Y-%m-%dT%H:%M:%S.%f')
    #datenew = datetime_master.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    ##neha
    print("dateobs:", dateobs)
    try:
        datetime_master = datetime.strptime(dateobs, '%Y-%m-%d"T"%H:%M:%S.%f')
    except:
        try:
            datetime_master = datetime.strptime(dateobs, '%Y-%m-%dT%H:%M:%S.%f')
        except:
            datetime_master = datetime.strptime(dateobs, '%Y-%m-%dT%H:%M:%S')
    #if 12<datetime_master.hour<18: hour_new=datetime_master.hour-12  #time is wrongly written
    #datetime_master=datetime_master.replace(hour=hour_new)
    #print(datetime_master,hour_new,'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    datenew = datetime_master.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    return datenew


def modify_dateobs(header, extn=0):
    """
    Modifies the value of DATE_keyword (i.e. time of observation) in the FITS header of multi-extension FITS
    files (Kinetic Mode Images).
    Args:
        header : FITS header which has to be modified for the time of observation
    Returns:
        header : Modified FITS header with the updated value of DATE_keyword
    """
    dateobs = header[DATE_keyword]
    datetime_master = datetime.strptime(dateobs, '%Y-%m-%dT%H:%M:%S.%f')
    datetime_new = datetime_master + extn * timedelta(seconds=header['ACT'])
    header[DATE_keyword] = datetime_new.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

    return header

# ------------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------------------------- #
# Functions for Homogenizing and Updating missing Header Keywords
# ------------------------------------------------------------------------------------------------------------------- #

def init_telescope(telescopename):
    """
    Defines a Telescope object in Ephem.
    Args:
        telescopename : Name of the Telescope from which the data was observed
    Returns:
        telescope     : Ephem.Observer object containing Telescope site details
    """
    _, OBS_LONG, OBS_LAT, OBS_ALT, _, _, _ = telescope_df.loc[telescopename].values

    telescope = ephem.Observer()
    telescope.lon = OBS_LONG
    telescope.lat = OBS_LAT
    telescope.elevation = OBS_ALT
    telescope.pressure = 0
    telescope.epoch = ephem.J2000

    return telescope


def append_nullheader(telescopename, filename):
    """
    Append Observatory details to the header of the file 'filename'
    Args:
        telescopename : Name of the Telescope from which the data was observed
        filename      : FITS file whose header has to be appended
    Returns:
        None
    """
    with fits.open(filename, mode='update') as hdulist:
        header = hdulist[0].header
        header.remove('OBJECT', ignore_missing=True, remove_all=True) #neha
        #print(keywords_df.index)
        #print(header.keys())
        for keyword in keywords_df.index:
            if keyword not in list(header.keys()):
                #print(keyword, "-------------")
                #print(keywords_df.loc[keyword, 'Value'])
                #print(header.keys) #neha
                header.append(card=(keyword, keywords_df.loc[keyword, 'Value']))
                #print("success")
        print("Null Headers updated")
        #print(header)
        #print("su 3---------")

def append_templatefiledetails(filename):
    """
    Append Filter details onto the header of the file 'filename'.
    Args:
        filename : FITS file to which filter details have to be appended.
    Returns:
        None
    """
    print("success----2 ------------")
    if filename in header_df.index:
        with fits.open(filename, mode='update') as hdulist:
            header = hdulist[0].header
            columns = header_df.columns
            for column in columns:
                val = header_df.loc[header_df.index == filename, column].values[0]
                if column.upper() in header.keys():
                    header.set(column.upper(), str(val).upper(), '')
    else:
        display_text("ERROR: File {0} not logged in {1}".format(filename, file_template))
        pass


def fix_invalidheaders(filename):
    """
    Filter invalid Header keywords from the FITS header.
    Args:
        filename      : FITS file whose header has to be appended
    Returns:
        None
    """
    fixed_hdul = fits.HDUList()

    with fits.open(filename) as hdulist:
        for hdu in hdulist:
            try:
                # First try to fix the fixable cards using 'fix' verification
                hdu.verify('fix')
            except:
                # Handle exception thrown due to non-fixable cards
                try:
                    # The error message of 'exception' verification will inform which cards have problem
                    hdu.verify('exception')
                except fits.VerifyError as err:
                    err_str = str(err)
                    # Find all cards from the error message where FITS standard error occured
                    match_iterator = re.finditer(r"Card \'(.+)\' is not FITS standard", err_str)

                    count = 0  # Count items in match_iterator
                    for match in match_iterator:
                        count += 1
                        # Check if this error is due to invalid value string
                        # i.e. possibly non-ASCII string since it couldn't be fixed
                        if match.group() + " (invalid value string:" in err_str:
                            # Fetch card's key & replace its value with empty string
                            hdr_key = match.group(1)
                            hdu.header[hdr_key] = ""
                            print(repr(hdu.header))  # WORK-AROUND: The header has to be printed to save changes
                            print("-" * 60)

                    if count == 0:  # If the match_iterator is empty, there's some unhandlable error
                        raise err

            fixed_hdul.append(hdu)

        # Save the changes to fix fixable cards while saving
        fixed_hdul.writeto("fixed_{0}".format(filename), output_verify='fix', overwrite=True)


def format_header(telescopename, filename):
    """
    Formats and homogenizes the header of the file 'filename'. Kinetic mode files are sliced into different FITS
    files and DATE_keyword is updated accordingly.
    Args:
        telescopename : Name of the Telescope from which the data was observed
        filename      : FITS file whose header has to be appended
    Returns:
        None
    """
    instrument = identify_instrument(instrument_df, filename)
    hdulist = fits.open(filename, mode='update')
    header = hdulist[0].header
    header['ORIGFILE'] = filename

    print('step111111111111111',telescopename)
    if telescopename == 'ST':
        #if instrument == '1k x 1k Imager':   #Neha
        if instrument == '1K_IMG2POL':        #Neha
            date = header['DATE_OBS'].replace('/', '-')
            print(date,'++++++++++++++++++++++++')
            time_utc = header['TIME']
            dateobs = format_dateobs(date + 'T' + time_utc)
            print(dateobs,'$$$$$$$$$$$$$$$$$$$$$')
            header[DATE_keyword] = dateobs 
            #header.extend(cards=(DATE_keyword, dateobs), update=True)
            #header.remove('OBJECT', ignore_missing=True, remove_all=True)
            print('test++++++++++++++++++++++++')

    elif telescopename == 'DFOT':
        if 'FRAME' in header.keys():
            header[DATE_keyword] = format_dateobs(header['FRAME'])
        elif 'DATE' in header.keys():
            header[DATE_keyword] = format_dateobs(header['DATE'])
        else:
            display_text("ERROR: DATE keyword not found in the Header")
            pass
            # sys.exit(1)

    if 'EXPOSURE' in header.keys():
        header[EXPOSURE_keyword] = header['EXPOSURE']
        header.remove('EXPOSURE', remove_all=True)

    if int(header['NAXIS']) == 3:
        if int(header['NAXIS3']) == 1:
            hdulist[0].data = extract_extndata(hdulist)
        else:
            for extn in range(0, int(header['NAXIS3'])):
                datanew = extract_extndata(hdulist, extn=extn)
                headernew = modify_dateobs(header.copy(), extn=extn)
                hdunew = fits.PrimaryHDU(data=datanew, header=headernew)
                hdunew.writeto("{0}_{1}.fits".format(filename.split('.')[0], extn + 1), overwrite=True)

    hdulist.flush()
    hdulist.close()


def append_telescopedetails(telescopename, instrument_df, filename):
    """
    Append Observatory details to the header of the file 'filename'
    Args:
        telescopename : Name of the Telescope from which the data was observed
        instrument_df : Pandas DataFrame containing Master-list of Instruments
        filename      : FITS file whose header has to be appended
    Returns:
        None
    """
    _, OBS_LONG, OBS_LAT, OBS_ALT, OBS_TIMEZONE, HORIZON, ZENITH = telescope_df.loc[telescopename].values
    instrument_df = instrument_df.loc[telescopename]

    instrument = identify_instrument(instrument_df, filename)
    if instrument in instrument_df['Instrument'].values:
        INSTRUME, PIXSCALE, RNOISE, GAIN, _, _ = instrument_df.loc[instrument_df['Instrument'] == instrument].values[0]

        dict_append = {'TELESCOP': telescopename, 'GEOLONG': OBS_LONG, 'GEOLAT': OBS_LAT, 'GEOELEV': OBS_ALT,
                       'HORIZON': HORIZON, 'ZENITH': ZENITH, 'TIMEZONE': OBS_TIMEZONE, 'INSTRUME': INSTRUME,
                       'PIXSCALE': PIXSCALE, 'DET-READ': RNOISE, 'DET-GAIN': GAIN}

        with fits.open(filename, mode='update') as hdulist:
            header = hdulist[0].header
            for keyword, value in dict_append.items():
                header[keyword] = value
    else:
        pass


def append_astrometryheader(filename):
    """
    Append Astrometry Keywords to the header of the file 'filename'. Also, compute central RA and DEC
    using those keywords and append them to the header
    Args:
        filename : FITS file to which Astrometry header details have to be appended
    Returns:
        None
    """
    new_filename = filename.split('.')[0] + '.new'
    headernew = fits.getheader(new_filename, ext=0)
    w = wcs.WCS(new_filename, naxis=2)
    radec = w.wcs_pix2world(headernew['NAXIS1'] / 2, headernew['NAXIS2'] / 2, 1)

    astrometrykeys = ['WCSAXES', 'CTYPE1', 'CTYPE2', 'CRVAL1', 'CRVAL2', 'CRPIX1', 'CRPIX2',
                      'CUNIT1', 'CUNIT2', 'CD1_1', 'CD1_2', 'CD2_1', 'CD2_2']

    with fits.open(filename, mode='update') as hdulist:
        header = hdulist[0].header

        for keyword in astrometrykeys:
            header.remove(keyword, ignore_missing=True, remove_all=True)
            header.append(card=(keyword, headernew[keyword]))

        for idx, keyword in enumerate([RA_keyword, DEC_keyword]):
            header.remove(keyword, ignore_missing=True, remove_all=True)
            header. append(card=(keyword, str(radec[idx])))


def calculate_airmass(telescopename, filename):
    """
    Calculates AIRMASS for the FITS file and appends respective details in the header of the file 'filename'
    Args:
        telescopename : Name of the Telescope from which the data was observed
        filename      : FITS file whose header has to be edited
    Returns:
        None
    """
    hdulist = fits.open(filename, mode='update')
    header = hdulist[0].header

    date_obs = header[DATE_keyword]
    object_ra = header[RA_keyword]
    object_dec = header[DEC_keyword]
    
    date_obs, time_utc = date_obs.split('T')
    datetime_utc = str(date_obs) + ' ' + str(time_utc)
    julian_day = ephem.julian_date(str(datetime_utc))

    telescope = init_telescope(telescopename)
    telescope.date = datetime_utc
    time_sidereal = telescope.sidereal_time()

    object_obs = ephem.FixedBody()
    object_obs._ra = object_ra
    object_obs._dec = object_dec
    object_obs._epoch = ephem.J2000
    object_obs.compute(telescope)

    lon= header['GEOLONG']
    lat= header['GEOLAT']
    c = SkyCoord(lon, lat, frame = 'icrs', unit = 'deg')
    lon = c.ra.value
    lat = c.dec.value
    lst = str(time_sidereal)
    LST = Angle(lst + ' hours').deg
    # Alt & Az calculated based on equations of http://www.stargazing.net/kepler/altaz.html
    # Also see the calculator: http://jukaukor.mbnet.fi/star_altitude.html
    ha = LST - float(object_ra)
    if ha < 0.0: ha = ha + 360
    sin_dec = np.sin(np.radians(float(object_dec)))
    sin_lat = np.sin(np.radians(lat))
    cos_lat = np.cos(np.radians(lat))
    cos_dec = np.cos(np.radians(float(object_dec)))
    # Altitude:
    alt0 = sin_dec * sin_lat + cos_dec * cos_lat * np.cos(np.radians(ha))
    alt1 = np.arcsin(alt0)     #in radians
    alt  = np.degrees(alt1)    #in degrees
    sin_alt = alt0
    cos_alt = np.cos(np.radians(alt))
    #Azimuth:
    az0 = np.arccos( (sin_dec - sin_alt*sin_lat) / (cos_alt*cos_lat ))
    if np.sin(np.radians(ha))<0: az = np.degrees(az0)
    else: az = 360 - np.degrees(az0)
    airmass = 1 / np.cos(np.radians(90 - alt))
    alt_angle = Angle(alt, u.deg).to_string(unit = u.degree, sep=':')
    az_angle = Angle(az, u.deg).to_string(unit = u.degree, sep=':')
    #dict_header = {'JD': str(julian_day), 'LST': str(time_sidereal), 'ALTITUDE': str(object_obs.alt),
                  # 'AZIMUTH': str(object_obs.az), 'AIRMASS': str(airmass)}
    dict_header = {'JD': str(julian_day), 'LST': str(time_sidereal), 'ALTITUDE': alt_angle,
                   'AZIMUTH': az_angle, 'AIRMASS': str(airmass)}
    for keyword, value in dict_header.items():
        if keyword in header.keys():
            header.remove(keyword, ignore_missing=True, remove_all=True)
        header.append(card=(keyword, value))

    hdulist.flush()
    hdulist.close()

# ------------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------------------------- #
# Functions for Performing Astrometry
# ------------------------------------------------------------------------------------------------------------------- #

def get_LST(telescopename, time_obs):
    """
    Calculates Local Sidereal Time for a 'telescope' at time specified in utc by 'time_obs'.
    Args:
        telescopename : Name of the Telescope from which the data was observed
        time_obs      : Time of observation in UTC
    Returns:
        LST_deg       : LST in degrees
    """
    date_obs, time_utc = time_obs.split('T')
    datetime_utc = str(date_obs) + ' ' + str(time_utc)

    telescope = init_telescope(telescopename)
    telescope.date = datetime_utc

    LST_hms = telescope.sidereal_time()
    LST_hms = str(LST_hms).split(':')
    LST_deg = (float(LST_hms[0]) * 1.0 + float(LST_hms[1]) / 60.0 + float(LST_hms[2]) / 3600.0) * 360.0 / 24.0

    return LST_deg


def do_astrometry(telescopename, filename, pixtolerance=0.02):
    """
    Performs Astrometry on images with constraints specified by RA and DEC if UT is specified.
    Args:
        telescopename : Name of the Telescope from which the data was observed
        filename      : FITS file on which Astrometry has to be performed
        pixtolerance  : Platescale tolerance in percentage
    Returns:
        None
    """
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    _, _, OBS_LAT, _, _, _, _ = telescope_df.loc[telescopename].values

    header = fits.getheader(filename, ext=0)
    date_obs = header[DATE_keyword]
    #print(header[OBJECT_keyword],'**************')
    #print(header['CATEGORY'],'*****************')
    #if header[OBJECT_keyword] in ['BIAS', 'FLAT']:
        #header['CATEGORY'] = 'Calibration':
    #    print('calibration file ******')
    #    pass

    #else:
    print('doing astrometry ******')
    try:
        PIXSCALE = header['PIXSCALE']
        PIX_l = str(PIXSCALE - (PIXSCALE * pixtolerance))
        PIX_u = str(PIXSCALE + (PIXSCALE * pixtolerance))

        LST_deg = get_LST(telescopename, date_obs)
        print(LST_deg,date_obs,'LST_deg & date_obs')
        # if telescopename == 'DFOT':
        try:
            subprocess.call('solve-field --continue --downsample 2 --no-plots --scale-low ' + PIX_l + ' --scale-high '
                            + PIX_u + ' --scale-units app --config '+DIR_DOC+'Astrometry.cfg --ra ' + str(LST_deg) + ' --dec ' +
                            str(OBS_LAT) + ' --radius 100 ' + filename, timeout=60, shell=True)
        except subprocess.TimeoutExpired:
            display_text("Astrometry Timed Out For '{0}'".format(filename))
            return False
        else:
            display_text("Astrometry Ran Sucessfully For '{0}'".format(filename))
            os.system('rm -rf *.axy *.corr *.xyls *.match *.rdls *.solved *.wcs')
            return True
        print('Astrometry successfull---------------------------111--') 
        # elif telescopename == 'ST':
        #    os.system('solve-field --continue --downsample 2 --no-plots --scale-low ' + PIXSCALE_l + ' --scale-high '
        #              + PIXSCALE_u + ' --scale-units app --config Astrometry.cfg  ' + filename)
        # else:
        #    sys.exit(1)
    except KeyError:
        display_text("ERROR: Header Keyword 'PIXSCALE' not found")
        return False
    print('Astrometry successfull-----------------------------')


def pmitofits(list_files, list_pmi='ListPMI'):
    """
    """
    with open(list_pmi, 'w') as f:
        for file_pmi in list_files:
            f.write(str(file_pmi) + '\n')
    os.system("./pmi2fits < {0}".format(list_pmi))

# ------------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------------------------- #
# Functions to Execute Code
# ------------------------------------------------------------------------------------------------------------------- #



# def check_astrometry(filename):

#     """ 
#     Checks whether astrometry is done on the files or not. If astrometry failed on a
#     source, it moves the file to the failed_astrometry/ directory.
#     """
#     if ('fits' in filename):
#             data=fits.open(filename)
#             header=data[0].header
#             try:
#                 ra,dec=header['RA'],header['DEC']
#                 filters=header['FILTER1']
#                 category=header['CATEGORY']
#                 if (category=='Science'):
#                     if (ra=='NULL'):
#                         print(filename,ra,dec,filters,'\t','astrometry failed')
#                         #shutil.move(filename,'failed_astrometry/')
#                     else:
#                         print(filename,ra,dec,filters, '\t','astrometry successful')
           
#             except KeyError:
#                 print(filename,filters,'\t','astrometry failed')
#                 pass



# def rename_files(filename):
#             data=fits.open(filename)
#             header=data[0].header
#             image=data[0].data
#             obj = header['OBJECT']
#             date_obs = header['DATE-OBS']
#             telescope = header['TELESCOP']
#             instru = header['INSTRUME']
#             if (obj == 'flat' or obj == 'FLAT' or obj == 'Flat'):
#                 code = 'F'
#             elif (obj == 'bias' or obj == 'BIAS' or obj == 'Bias'):
#                 code = 'B'
#             elif (obj == 'test' or obj == 'TEST' or obj == 'Test'):
#                 code = 'T' 
#             else:
#                 code = 'S'
#             new_name=code+'-2019APXX-'+date_obs+'-'+telescope+'-'+instru+'.fits'
#             try:
#                 os.rename(filename,new_name)
#             except FileNotFoundError:
#                 pass
#             #print(header.keys())

#             (prefix, sep, suffix) = new_name.rpartition('.')
#             thumb_name=prefix
#            # print(thumb_path+'/{}.png'.format(thumb_name))

#             if ('CRVAL1' in header.keys()):
#                 print(filename,'astrometry done')
#                 try:
#                     f1=aplpy.FITSFigure(new_name)
#                     f1.show_grayscale()
#                     f1.axis_labels.set_xtext('RA (J2000)')
#                     f1.axis_labels.set_ytext('Dec (J2000)')
#                     f1.save('thumbnails/{}.jpg'.format(thumb_name),dpi=60)
#                     print('Thumbnail saved!!')
      
#                 except KeyError:
#                     print("Keyword issue!")     
#                 except TypeError:
#                     print ("Kinetic mode image..no thumbnail generated!!!")      
             

def execute_task(ctext, telescopename):
    """
    Updates and Homogenizes Header Details of Optical Data from ST, DFOT and DOT.
    Args:
        ctext         : Common text of FITS files on which the header updation has to be performed
        telescopename : Name of the Telescope from which the data was observed
    Returns:
        None
    """
    # Performs homogenizing and updating the Header
    for filename in glob.glob(ctext):
        print("filname:::::::::::::::::::", filename)
        append_nullheader(telescopename, filename)
        print("******* Step 1: Null header done")
        append_templatefiledetails(filename)
        print("******* Step 2: template header done ")
        append_telescopedetails(telescopename, instrument_df, filename)
        print("******* Step 3: telescope header ")
        format_header(telescopename, filename)
        print("******* Step 4: format header ")
        # fix_invalidheaders(filename)

    # Performs Astrometry and updates the Header with Astrometry Keywords
    for filename in glob.glob(ctext):
        if identify_imagetype(filename):
            print("******* Step 5: start astrometry ")
            if do_astrometry(telescopename, filename):
                print("******* Step 6: appending astrometry header ")
                append_astrometryheader(filename)
                print("******* Step 7: astrometry done ")
                calculate_airmass(telescopename, filename)
                print("******* Step 8: successful")
            
        #check_astrometry(filename)
        #print('************* Step 9: astrometry check done')
        #rename_files(filename)
        #print('******** Step 10: File has been renamed')


def main():
    """
    Step 1: GUI Code
    Step 2: Group FITS files and Formats and Appends details to the Header
    """
    # Manual Setup - GUI Code
    # --------------------------------------------------------------------------------------------------------------- #
    #TELESCOPE = eg.choicebox(msg='Select The Name of the Telescope!', title='Name of the Telescope',
     #                         choices=telescope_df.index.values)
    #     os.path.join(root, filename)

    ctext = '*.fits' 
    TELESCOPE = 'DFOT'

    # Convert .PMI to .FITS

    # Run the Tasks on All the Files in the Directory
    # --------------------------------------------------------------------------------------------------------------- #
    execute_task(ctext, TELESCOPE)
    # for root, dirs, files in os.walk(directory):
    #     if group_similar_files('ListFiles', '*.pmi'):
    #         pmitofits(group_similar_files('ListFiles', '*.pmi'):)
    #         execute_task('*.fits', TELESCOPE)
    #     elif group_similar_files('ListFiles', '*.fits'):
    #         execute_task('*.fits', TELESCOPE)

# ------------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------------------------- #
# Run the Code
# ------------------------------------------------------------------------------------------------------------------- #
if __name__ == '__main__':
    main()
# ------------------------------------------------------------------------------------------------------------------- #
