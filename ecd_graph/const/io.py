import os
import sys
import shutil


def create_folder(graph_directory):

    directory = graph_directory   

    if os.path.exists(directory):
        if input(f'A directory named {directory} already exists. Existing directory  will be deleted, wanna procede? [y/n]').lower() in ['y', 'ye', 'yes']:
            shutil.rmtree(directory)   
        else:
            sys.exit()
    os.mkdir(directory)

    return
