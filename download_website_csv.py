import csv
from bs4 import BeautifulSoup
from pylab import *
import requests
from datetime import datetime, timedelta
import time
import pandas as pd

def download_website():
    # Download the website
    url = 'https://www.aries.res.in/130cm-publicationlist/1.3m_log/show_observation_log.php'
    response = requests.get(url,verify=False)
    with open('website.html', 'w') as f:
        f.write(response.text)
    print(f'Website downloaded at {datetime.now()}')

download_website()

with open("website.html") as f:
    soup = BeautifulSoup(f, "html.parser")
table = soup.find("table")


with open("table_latest.csv", "w") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow([th.text for th in table.find("tr").find_all("th")])
    for row in table.find_all("tr")[1:]:
        csv_writer.writerow([td.text for td in row.find_all("td")])

observer=np.genfromtxt('table_latest.csv',usecols=1,delimiter=',',dtype=str,skip_header=1)
date=np.genfromtxt('table_latest.csv',usecols=0,delimiter=',',dtype=str,skip_header=1)

date=[i.replace('-','') for i in date]
date=[int(i) for i in date]
print('Observer: ',observer[0:20])
print('Date: ',date[0:20])


# # Set the time when the website should be downloaded
# download_time = datetime.strptime('09:00:00', '%H:%M:%S').time()

# while True:
#     current_time = datetime.now().time()
#     if current_time > download_time:
#         download_website()
#         # Set the time for next day's download
#         download_time = download_time + timedelta(days=1)
#     time.sleep(60) # Sleep for a minute before checking the time again


# 
# print(name[0:100])


### Plot the latest hitogram for the observations using the observation log.

date_strings=np.genfromtxt('table_latest.csv',usecols=0,delimiter=',',dtype=str,skip_header=1)

years=[]
date_format = "%Y-%m-%d"
for i, date_string in enumerate(date_strings):
    if i == 0 or date_string != date_strings[i - 1]:
        years.append(datetime.strptime(date_string, date_format).year)



fig,ax = plt.subplots()
bins = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
counts, bin_edges = np.histogram(years, bins=bins)
bin_centers = (bin_edges[:-1])# + bin_edges[1:])/2
ax.bar(bin_centers,counts,color='darkgreen',alpha=0.83,edgecolor='black')
ax.plot(bin_centers,counts,color='black',ls='-.',  lw=2)
ax.plot(bin_centers,counts,color='red',marker='o',markersize=10,lw=0)
#ax.hist(years,bins=bins,color='darkgreen',align='left', edgecolor='white', lw=5)
ax.set_xlabel('Observation year',fontsize=25)
ax.set_ylabel('No. of days observed',fontsize=25)
ax.set_title('1.3m DFOT Observations',fontsize=30)
ax.tick_params(axis="both",which='minor',direction="in")
ax.tick_params(axis="both",which='major',direction="in")
ax.yaxis.set_ticks_position('both')
ax.minorticks_on()
plt.xticks(bins)
plt.show()