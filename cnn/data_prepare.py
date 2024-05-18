import os
import shutil

from cnn.constants import *


def create_directory(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)
    os.makedirs(os.path.join(dir_name, FIRST_CLASS_NAME))
    os.makedirs(os.path.join(dir_name, SECOND_CLASS_NAME))


def copy_images(start_index, end_index, source_dir, dest_dir):
    for i in range(start_index, end_index):
        try:
            shutil.copy2(os.path.join(source_dir, fr'{FIRST_CLASS_NAME}\img_0_{i}.jpg'),
                         os.path.join(dest_dir, FIRST_CLASS_NAME))
        except FileNotFoundError:
            print(i)
        try:
            shutil.copy2(os.path.join(source_dir, fr'{SECOND_CLASS_NAME}\img_0_{i}.jpg'),
                         os.path.join(dest_dir, SECOND_CLASS_NAME))
        except FileNotFoundError:
            print(i)
