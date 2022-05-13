import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mp

#~~~~~~~~~~~~~~~~ For Plotting only~~~~~~~~~~#
mp.rcParams['font.family']='serif'
mp.rcParams['xtick.major.size']=10
mp.rcParams['xtick.major.width']=2
mp.rcParams['xtick.minor.size']=7
mp.rcParams['xtick.minor.width']=2
mp.rcParams['ytick.major.size']=10
mp.rcParams['ytick.major.width']=2
mp.rcParams['ytick.minor.size']=7
mp.rcParams['ytick.minor.width']=2
mp.rcParams['axes.linewidth']=1.5
mp.rcParams['xtick.labelsize']=15
mp.rcParams['ytick.labelsize']=20
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

no_of_obs=np.genfromtxt('all_data.txt',usecols=1,dtype=float)
name=np.genfromtxt('all_data.txt',usecols=0,dtype=str)



fig,ax = plt.subplots()
#ax = fig.add_axes([0.1, 0.1, 0.8, 0.8]) 
ax.bar(name,no_of_obs,color='teal',alpha=0.83,edgecolor='black')
ax.plot(name,no_of_obs,color='black',ls='-.',  lw=2)
ax.plot(name,no_of_obs,color='red',marker='o',markersize=10,lw=0)
ax.set_xlabel('Observation year',fontsize=25)
ax.set_ylabel('No. of days observed',fontsize=25)
# setting title of plot
ax.set_title('1.3m DFOT data',fontsize=30)
# set the tick marks for x axis
#ax.set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
# provide name to the x axis tick marks
#ax.set_xticklabels(name)
#ax.set_yticks([-1,0,1])
ax.legend(fontsize=30)
ax.tick_params(axis="both",which='minor',direction="in")
ax.tick_params(axis="both",which='major',direction="in")
ax.yaxis.set_ticks_position('both')
#ax.xaxis.set_ticks_position('both')
ax.minorticks_on()

plt.show()