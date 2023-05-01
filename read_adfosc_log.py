import numpy as np
from astropy.time import Time

#MJD, Temperature, Humidity, RA,Dec, Airmass, Altitude, Azimuth, Rotator

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
                t = Time(datetime_string, format='isot', scale='utc')
                t.format = 'fits'
                print(f"date_time: {t}, Position: {mapped_position}, Param: {param[num]}")


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

            print(output)



read_adfosc('ics_log.txt')
read_telnet('telnet_log.txt')