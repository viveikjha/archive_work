import os

path = '/data/astro_data/final_data/2023/Apr/DFOT/2K_IMG1/'
extensions = ('.dat', '.py', '.txt', '.new')

for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(extensions):
            os.remove(os.path.join(root, file))
