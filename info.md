
This repository is meant to be a testing place for the codes/arguments executed by me. This is a git repostory (can push/pull files from the local computer and sync with the archive and on the Git server). 
 
# Steps so far:

- I have gone through the archive and some seasons are missing from the 1.3m database. Thee data may not be retrieved.

- Some of the files remain where astrometry has not been done so far. We need to mark them and perform astrometry on these data files. (Not done yet)

- Files need to be renamed ASAP according to the convention we have developed for the archive. Example: S-2020C2P74-20180121T11:20:21.13-DOT-ADFOSC.FITS
We need to transfer the best quality data to the archive PC asap and then transfer it further towards the database for a quick demo.


 *Problem:* What if some files have missing parameters in the fits name convention?

- The folder structure as discussed will be: xxx/yyy/final_data/year_name/month_name/telescope/instrument/files

example: /data/final_data/2022/Jan/DOT/TANSPEC/


In order to remove empty folders and subfolders we may use this snippet.



~~~python
import os

root = 'FOLDER'
folders = list(os.walk(root))[1:]

for folder in folders:
    # folder example: ('FOLDER/3', [], ['file'])
    if not folder[2]:
        os.rmdir(folder[0])

~~~



The files on the archive PC have been sorted now. Three folders will be present:
- The RAW folder contains all the raw data that is directly imported from the telescope.
- The processed_data folder contains all the data that is being used for the processing needs. Here we may keep all the files that have not been succesful for the archives (files with missing filter information for instance.)
- The final_data folder is the one that can be taken for the database being used in the archive. 

