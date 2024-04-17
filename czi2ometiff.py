#!/bin/python3

import sys
import os
from aicsimageio import AICSImage
from aicsimageio.types import PhysicalPixelSizes
import numpy as np

dir_czi = '/path/to/inputdir_czi_files/'
dir_ometiff = '/path/to/outputdir_ometiffs/'

files_czi = ['imaging_file_1.czi',
             'imaging_file_2.czi']

for file in files_czi:
        
        print(file)
        AICSImage(dir_czi + file).save(dir_ometiff + (str(file).split('.')[0] + '.ome.tiff'))
