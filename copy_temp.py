import os
import shutil

root_dir = '/data/astro_data/processed_data/DFOT/2023A/Mar/'
filename='gen_template.py'

source_file = '/data/astro_data/processed_data/DFOT/2023A/gen_template.py'

folder_iter = os.walk(root_dir)
for current_folder, _, _ in folder_iter:
    destination_file = os.path.join(current_folder, filename)
    try:
        os.remove('*.py')
    except:
        pass
    shutil.copy2(source_file, destination_file)