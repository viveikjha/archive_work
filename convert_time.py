
from astropy.time import Time
import os
import glob

files = glob.glob('*.txt')
for file in files:
    if 'adfosc' in file or 'telnet' in file:
        date_time_str = file.split("_")[3:9]
        date_time_str = "-".join(date_time_str[:3]) + "T" + ":".join(date_time_str[3:]).split(".")[0]
        t = Time(date_time_str, format='isot', scale='utc')
        new_file_name = file.replace(date_time_str.replace("T", "_").replace("-", "_").replace(":", "_"), t.isot)
        os.rename(file, new_file_name)


# from astropy.time import Time
# import os

# file = "adfosc_telnet_log_2023_01_21_09_19_57.txt"
# date_time_str = file.split("_")[3:9]
# date_time_str = "-".join(date_time_str[:3]) + "T" + ":".join(date_time_str[3:]).split(".")[0]
# t = Time(date_time_str, format='isot', scale='utc')
# new_file_name = file.replace(date_time_str.replace("T", "_").replace("-", "_").replace(":", "_"), t.isot)
# print(new_file_name)



# file = "tcs_telnet_log_2023_01_21_17_20_21.txt"
# date_time_str = file.split("_")[3:9]
# date_time_str = "-".join(date_time_str[:3]) + "T" + ":".join(date_time_str[3:]).split(".")[0]
# t = Time(date_time_str, format='isot', scale='utc')
# new_file_name = file.replace(date_time_str.replace("T", "_").replace("-", "_").replace(":", "_"), t.isot)
# print(new_file_name)
