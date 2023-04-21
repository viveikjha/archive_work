import numpy as np
from astropy.time import Time

with open ('telnet_log.txt', 'r') as log:
    text=log.read()
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

        all_data = tcsdata + tcsmount + tcsweather
        # date_str = tcsdata['date']
        # time_str = tcsdata['time']
        # day, month, year = date_str.split('/')
        # date_string = '-'.join([year, month, day])
        # datetime_string = date_string + 'T' + time_str
        # t = Time(datetime_string, format='isot', scale='utc')
        # t.format = 'fits'   
        # print(t)
    # for data in tcsweather:
    #     print(data['time'])

          

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

    print(output)

