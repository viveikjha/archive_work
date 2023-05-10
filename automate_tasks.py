import os
import time
import operator
import shutil
from astropy.io import fits
import warnings
import aplpy
import datetime
import fnmatch




warnings.filterwarnings('ignore')

#def check_template_file(filename):

def prepare_the_files(filepath):
    '''
    This module searches for the latest folder in the cycle. It moves the folder to the processed_data folder. Once the data is in the processed data folder, a template file is generated there, which contains the information about the source name and the filter used. This template file is then used to update the headers and perform astrometry on the data.
    Input: Path of the parent folder where new data is stored. Hint: use os.getcwd() if the data is in the same folder.
    
    '''

    print('*******************************************')
    print(' Files being processed for the 2022B season.')
    print('Start time--->',datetime.datetime.now())
    alist={}
    now = time.time()

    os.chdir(filepath)

    for file in os.listdir("."):
        if os.path.isdir(file):
            timestamp = os.path.getmtime( file )
            # get timestamp and directory name and store to dictionary
            alist[os.path.join(os.getcwd(),file)]=timestamp

    for i in sorted(alist.items(), key=operator.itemgetter(1)):
        latest="%s" % ( i[0])



    print(' The latest data folder found is:', latest)
    folder_name=os.path.basename(latest)
    processed_path='/data/archived_data/processed_data/DFOT/2022B/'+folder_name

    template_generate='../src/gen_template.py'
    src_path='../src/Doc/'
    shutil.copytree(latest,processed_path)
    print(' Folder copied to processed data.')
    os.chdir(processed_path)
    shutil.copy(template_generate,processed_path)
    os.system("python gen_template.py >TemplateFileList.dat ")
    print('Template File for this date generated')
    with open (src_path+'dir_lst.txt', 'w') as file:  
        file.write(processed_path)  
        file.close()
    print(' New folder is ready to be processed')
    print('Starting the process now...')
    os.system('python '+ src_path + 'MasterRun.py')
    return folder_name

def check_astrometry(filepath):
    '''
    This module checks each file, and informs whether astrometry has been successfully run or not. If the astrometry is successful, it returns 'astrometry successful' as message and if it has failed, it moves the file to the 'failed_round1' directory.
    '''
    processed_path=folder_name
    failed_folder='failed_round1'
    kinetic_folder='kinetic'

    kinetic_path=os.path.join(processed_path,kinetic_folder)
    failed_path=os.path.join(processed_path,failed_folder)
    if os.path.exists(failed_path):
            shutil.rmtree(failed_path)
    os.mkdir(failed_path)

    if os.path.exists(kinetic_path):
            shutil.rmtree(kinetic_path)
    os.mkdir(kinetic_path)

    for path, subdirs, files in os.walk(processed_path):
        for file_name in files:
            name=os.path.join(path, file_name)
            col1=os.path.basename(name)
            
        
            if ('fits' in col1):
                
                #info=data[0].data
                try:
                    data=fits.open(name)
                    header=data[0].header
                    ra,dec=header['RA'],header['DEC']
                    filters=header['FILTER1']
                    category=header['CATEGORY']
                    orig=header['ORIGFILE']
                    if (category=='Science'):
                        if (ra=='NULL'):
                            print(name,filters,'\t','astrometry Failed')
                            shutil.copy2(name,failed_path)
                            os.remove(name)
                            print('\n file without astrometry moved \n ')
                        else:
                            print(name,ra,dec,filters, '\t','astrometry successful')
                    if (category=='Calibration'):
                        print(name,'calibration file only!')
                except OSError:
                    print(name,'Corrupt file')
                    try:
                        shutil.copy2(name, failed_path)
                        os.remove(name)
                    except shutil.SameFileError:
                        pass

                    continue
                except KeyError:
                    print(name,'\t','astrometry failed')
                    try:
                        shutil.copy2(name, failed_path)
                        os.remove(name)
                    except shutil.SameFileError:
                        pass
                try:
                    print(name,'kinetic mode:',header['NAXIS3'])
                    shutil.move(name, kinetic_path)

                except KeyError:
                    pass
                except shutil.Error:
                    pass
            print('astrometry check completed')

def rename_generate_thumbnails(filepath,cycle):

    '''
    This module renames the files as per the standard name convention for the ARIES telescopes and also generates the thumbnails for every science frame with succesful astrometry. The cycle keyword is needed to identify data from different cycles.
    '''
    root=os.getcwd()
    for path, subdirs, files in os.walk(filepath,topdown=False):
        count=0
        thumb_folder='thumbnails'
        thumb_path=os.path.join(path,thumb_folder)
        

        if os.path.exists(thumb_path):
            shutil.rmtree(thumb_path)
        os.mkdir(thumb_path)


        for file_name in files:
            name=os.path.join(path, file_name)
            col1=os.path.basename(name)
            dir_path=os.path.dirname(name)  
        


            if ('fits' in col1):
                print(' Generating thumbnails now')
                data=fits.open(name)
                header=data[0].header
                #image=data[0].data
                obj = header['OBJECT']
                date_obs = header['DATE-OBS']
                telescope = header['TELESCOP']
                instru = header['INSTRUME']
                if (obj == 'flat' or obj == 'FLAT' or obj == 'Flat'):
                    code = 'F'
                elif (obj == 'bias' or obj == 'BIAS' or obj == 'Bias'):
                    code = 'B'
                elif (obj == 'test' or obj == 'TEST' or obj == 'Test'):
                    code = 'T' 
                else:
                    code = 'S'
                new_name=code+'-'+cycle+'PXX-'+date_obs+'-'+telescope+'-'+instru+'.fits'
            
                #print(header.keys())

                (prefix, sep, suffix) = new_name.rpartition('.')
                thumb_name=prefix
            # print(thumb_path+'/{}.png'.format(thumb_name))

                if ('CRVAL1' in header.keys()):
                    #print(col1,'astrometry done')
                    try:
                        f1=aplpy.FITSFigure(name)
                        f1.show_grayscale()
                        f1.axis_labels.set_xtext('RA (J2000)')
                        f1.axis_labels.set_ytext('Dec (J2000)')
                        f1.save(thumb_path+'/{}.jpg'.format(thumb_name),dpi=60)
                        print('Thumbnail saved!!')
        
                    except KeyError:
                        #print("Keyword issue!")
                        continue
                    except TypeError:
                        print ("Kinetic mode image..no thumbnail generated!!!")
                        continue
                    try:
                        print(name,'kinetic mode:',header['NAXIS3'])
                        shutil.move(name, '/data/archived_data/processed_data/DFOT/2022A/kinetic_images2/')

                    except KeyError:
                        print(name)
                        
                print(count,':processed')
                os.rename(name,os.path.join(path,new_name))
                count+=1
                
        if not os.listdir(root[0]):
            os.remove(dirs(root[0]))

def move_to_final(filepath):

    ''' This module collects all the fits files and the puts them in the respective folder in the final_data folder. The data from this folder can be uploaded to the archive database instanly after that.
    '''
    print(' Moving the files to the final directory now.')
    final_folder=os.path.basename(filepath)
    folder=str(final_folder)
    month_num = str(folder[4:6])
    datetime_object = datetime.datetime.strptime(month_num, "%m")
    month_name = datetime_object.strftime("%b")
    final_path='/data/archived_data/final_data/2022/'+month_name+'/DFOT/2K_IMG1/'+final_folder
    test='test'
    shutil.copytree(filepath,final_path)
    os.chdir(final_path)
    os.system('rm -rf *new *py *dat *match *wcs *rdls *corr ')
    os.system('rm -rf failed_round1')
    os.system('rm -rf kinetic')
    count_files = len(fnmatch.filter(os.listdir(final_path), '*.fits*'))
    print(" Folder name '{}' with '{}' fits files have been put in the final folder".format(final_folder,count_files))
    print('Process completed. The data is ready for the archive.')
    print('End time--->',datetime.datetime.now())
    print('*******************************')


filepath=os.getcwd()
prepare_the_files(filepath)
folder_name=os.getcwd()
check_astrometry(folder_name)
rename_generate_thumbnails(folder_name,'2022B')
move_to_final(folder_name)

'''
for cron job. This one line script should be sufficent:
*/1 * * * * /home/archive/anaconda3/bin/python /data/archived_data/raw_data/DFOT/2022B/date.py >> /data/archived_data/raw_data/DFOT/2022B/log.txt
'''