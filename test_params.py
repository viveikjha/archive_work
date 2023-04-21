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



with open ('ics_log.txt', 'r') as log:
    text=log.read()
   
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
                    #print(key,mapped_position)
                    param=parameters[key]
                    num=int(number)
            date_string = date
            day, month, year = date_string.split('/')
            date_string = '-'.join([year, month, day])
            datetime_string = date_string + 'T' + time
            t = Time(datetime_string, format='isot', scale='utc')
            t.format = 'fits'

            #print(f"Date: {date}, Time: {time}, Position: {position}, Number: {number}")
            print(f"T: {t}, Position: {mapped_position}, Param: {param[num]}")