import numpy as np
import os
path,type,filter=np.genfromtxt('detailed_list.dat',unpack=True,usecols=(0,1,2),dtype=str,skip_header=1)
date=[]
for i in range(len(path)):
    k=path[i]
    name=os.path.basename(k)
    date.append(k[41:49])


for i in range(len(path)):
    k=path[i]
    name=os.path.basename(k)
    if(date[i-1]==date[i]):
        print(name,type[i],filter[i])
    else:
        print('\n -------Template file for-------->',date[i],'\n')
