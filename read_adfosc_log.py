import numpy as np
from astropy.time import Time, TimeDelta
from astropy.io import fits
import glob
import os,sys
import time
import astropy.units as u

#MJD, Temperature, Humidity, RA,Dec, Airmass, Altitude, Azimuth, Rotator
log_path='/data/astro_data/raw_data/DOT/dot_adfosc/Log_ADFOSC_Telescope/'
fits_path='/data/astro_data/raw_data/DOT/dot_adfosc/2022-C2/2023-01-14/P23/'

adfosc_log=sorted(glob.glob(log_path+'*adfosc_ics*.txt'))
telnet_log=sorted(glob.glob(log_path+'*tcs_telnet*.txcd t'))
fits_files=sorted(glob.glob(fits_path+'*fit'))


parameters = {
    "NB": {
        0: "clear",
        1: "Small aperture",
        2: "H-beta",
        3: "BG3",
        4: "Low red H-alpha",
        5: "High red H-alpha",
        6: " ",
        7: " ",
        8: " ",
        9: " "
    },
    "SW": {
        0: "clear",
        1: "Brass large",
        2: "SS",
        3: "SS",
        4: "SS narrow",
        5: "Slit holder",
        6: " ",
        7: " ",
        8: " ",
        9: " "
    },
    "BB": {
        0: "z",
        1: "WP",
        2: "u",
        3: "BG39",
        4: "g",
        5: "RG610",
        6: "r",
        7: "Clear",
        8: "i",
        9: "Clear"
    },
    "GW": {
        0: "Clear",
        1: "770R-300g/mm",
        2: "132R-600g/mm",
        3: "460R-830.7g/mm",
        4: "676R-420g/mm",
        5: "Prism",
        6: "DIMM prism",
        7: "Clear",
        8: "100g/mm",
        9: "Clear"
    }
}

#for key in parameters:
    #print(key)
    #print(parameters[key])

# gw_parameter = parameters["GW"]
# nb_parameter = parameters["NB"]
# bb_parameter = parameters["BB"]
# sw_parameter = parameters["SW"]


name_map = {
'Broadband position': 'BB',
'Narrowband position': 'NB',
'Grism wheel position': 'GW', 
'Slit wheel position': 'SW'
}




def read_adfosc(file):
    with open(file, 'r') as log:
        text = log.read()
        t_list=[]
        map_pos=[]
        par_num=[]
        lines = text.split("\n")
        for line in lines:
            if line.strip() != "":
                parts = line.split(" ")
                date = parts[0]
                time = parts[1]
                position = " ".join(parts[2:-3])
                number = parts[-1]
                mapped_position = name_map.get(position, position)
                for key in parameters:
                    if mapped_position == key:
                        param = parameters[key]
                        num = int(number)
                       
                date_string = date
                day, month, year = date_string.split('/')
                date_string = '-'.join([year, month, day])
                datetime_string = date_string + 'T' + time
                t = Time(datetime_string, format='isot', scale='local')
                t.format = 'isot'
                #date_time=t.datetime
                #print(f"{t}, {mapped_position},{param[num]}")
                t_list.append(t.value)
                map_pos.append(mapped_position)
                par_num.append(param[num])
                #return({t}.isoformat())
        return t_list, map_pos, par_num
        
def read_telnet(file):
    with open(file, 'r') as log:
        text = log.read()
        lines = text.split('\n')
        tcsdata = []
        tcsmount = []
        tcsweather = []

        for line in lines:
            components = line.split()
            date_time = components[:2]

            if 'tcsdata' in components:
                data = dict(zip(['date', 'time', 'MJD', 'targetra', 'targetdec', 'airmass'], date_time + components[6:]))
                tcsdata.append(data)
            elif 'tcsmount' in components:
                data = dict(zip(['date', 'time', 'MJD', 'altitude', 'azimuth', 'rotator'], date_time + components[6:]))
                tcsmount.append(data)
            elif 'tcsweather' in components:
                data = dict(zip(['date', 'time', 'MJD', 'temperature', 'humidity'], date_time + components[6:]))
                tcsweather.append(data)

        for iteration in range(len(tcsdata)):
            data = tcsdata[iteration]
            mount = tcsmount[iteration]
            weather = tcsweather[iteration]

            output = []
            date_str = data['date']
            time_str = data['time']
            day, month, year = date_str.split('/')
            date_string = '-'.join([year, month, day])
            datetime_string = date_string + 'T' + time_str
            t = Time(datetime_string, format='isot', scale='utc')
            t.format = 'fits'

            output.append(f"date_time: {t}")
            output.append(f"MJD: {data['MJD']}")

            for key, value in data.items():
                if key not in ['date', 'time', 'MJD']:
                    output.append(f"{key}: {value}")
            for key, value in mount.items():
                if key not in ['date', 'time', 'MJD']:
                    output.append(f"{key}: {value}")
            for key, value in weather.items():
                if key not in ['date', 'time', 'MJD']:
                    output.append(f"{key}: {value}")

            #print(output)
            return(output)

def time_from_file(filename):
    data=fits.open(filename)
    header=data[0].header
    time=header['DATE-OBS']
    return time


times=[]

for i in range (len(fits_files)):
    time1=time_from_file(fits_files[i])
    times.append(time1)

log_time=np.genfromtxt('read_adfosc_log.dat',usecols=1,dtype=str)
delta=TimeDelta(5 * u.second)
for i in range (len(log_time)):
    log_td=Time(log_time[i])
    t1=log_td+delta
    t2=log_td-delta
    for j in range(len(times)):
        time_fits=Time(times[j])
        if t1<time_fits<t2:
            print(log_time[i],times[j])

# for lt, t in zip(log_time, times):
#     if lt != t:
#         print(lt, t)

# start_time = time.time()
# for i in range (len(adfosc_log)):

#     try:
#         a,b,c=read_adfosc(adfosc_log[i])
#         t = Time(a, format='isot', scale='utc')
#         date_string = [date.datetime.strftime('%d%m%Y') for date  in t]
#         result = [year_month for year_month in date_string if year_month == '15012023']
#         for k in range (len(result)):
#             for t in range (len(time))
#             print(result[k],a[k],b[k],c[k])
#     except:
#         pass

# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f" Searching ADFOSC log for a day executed in: {elapsed_time} seconds")

#Searching ADFOSC log for a day executed in: 1060.827548980713 seconds

print(times)  

#print(times)
# files=sorted(glob.glob("*fit"))
# len(files)
# for i in range (len(files)):
#     data=fits.open(files[i])
#     header=data[0].header
#     time=header['DATE-OBS']
#     print(files[i],time)



#files = glob.glob('*.txt')
def create_database(input_time,dir_path):
    time=input_time
    for file in dir_path:
        if 'adfosc_telnet' in file or 'tcs_telnet' in file:
            date_time_str = file.split("_")[3:9]
            date_time_str = "-".join(date_time_str[:3]) + "T" + ":".join(date_time_str[3:]).split(".")[0]
            t = Time(date_time_str, format='isot', scale='utc')
            new_file_name = file.replace(date_time_str.replace("T", "_").replace("-", "_").replace(":", "_"), t.isot)
            #os.rename(file, new_file_name)

            t = Time(new_file_name, format='isot')
            date = t.iso.split()[0]
            time = t.iso.split()[1]

            print(f"Date: {date}")
            print(f"Time: {time}")
