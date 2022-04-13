import os 
import easygui as eg
import numpy as np

#DIR_CYCLE = eg.enterbox(msg='Select The Cycle (Directory) for which the Code has to run!', title='Name of the Observational Cycle', default=os.getcwd())
# DIR_DOC = eg.enterbox(msg='Select The Directory in which Document Files are Stored!',
#                             title='Name of the Directory of Docs', 
#                             default='/home/avinash/Downloads/Codes/MasterAppend/')

#doc_files = '/home/sapna/ARIES_DataArchival/Data/Dummy/Doc/'
doc_files = '/home/bharti/data_archival_project/Dummy/Doc/'
#DIR_CYCLE += '/2015C/'

#ctext = '*.fits'
#TELESCOPE = 'DFOT'

# #for root, dirs, files in os.walk(DIR_CYCLE):
#     #x = [filename for filename in files if filename.endswith('.fits')]
#     #if [filename for filename in files if filename.endswith('.fits')]:
#     #    execute_task(root, '*.fits', TELESCOPE)
#     #    os.chdir(#dir_inside_cycle#)
        
#root,dirs,files = os.walk('/home/sapna/ARIES_DataArchival/Data/Dummy/15c/')
#print(root,dirs)


lst_dir = np.loadtxt('dir_lst',usecols=[0],unpack=True,dtype='str')

for ff in range(len(lst_dir)):
#for ff in range(0,1):
    os.chdir(lst_dir[ff])
    os.system('python3  '+doc_files+'AppendHeaderNew.py')
    
