import pandas as pd
import numpy as np
df=pd.read_csv('1.3m_obs_log.tsv',sep='\t')
filter=np.genfromtxt('1.3m_obs_log.tsv',unpack=True, delimiter='\t',usecols=4,dtype=str,skip_header=1)


observer=(df['OBSERVER'])
date=df['DATE (yyyy/mm/dd)']
date=[i.replace('-','') for i in date]
date=[int(i) for i in date]

operator=df['OPERATOR']
object=df['OBJECT']
#filter=df['FILTER']
single_filter=[]
new_date=[]
[single_filter.append(filters)  for filters in filter if len(filters)==1]

for i in range (0,len(filter)):
        if len(filter[i])==1 and date[i] > 20211101 and date[i] < 20211201:
            print(date[i],filter[i],observer[i],operator[i],object[i])