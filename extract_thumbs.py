import os
import shutil

src_dir = '/data/astro_data/final_data/'
dst_dir = '/data/thumbnails/'

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(('.png', '.jpg')):
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_dir, os.path.relpath(src_file, src_dir))
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)