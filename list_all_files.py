import os  
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
mp.rcParams['xtick.labelsize']=30
mp.rcParams['ytick.labelsize']=30
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

path=os.getcwd()

folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name))])

for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) >0: # if greater than the limit, print folder and number of contents
        print(folder,len(contents))
