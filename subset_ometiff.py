import sys
import os
from datetime import datetime
import time
from aicsimageio import AICSImage
from aicsimageio.types import PhysicalPixelSizes
import numpy as np

# Make a function to subset the input object by a specified z-slice range and write to OME-TIFF
def subsetczi_writeometiff(filepath, range_start, range_end):

    # The range values come from FIJI's numbering, so convert to values for 0-index
    actual_range_start = range_start - 1
    actual_range_end = range_end - 1

    z_dim = actual_range_end - actual_range_start

    # Constructor (making instance of the class and giving instance a place in memory)
    img = AICSImage(filepath)
    

    print("IMAAGE LOADED -- " + str(datetime.now()))
    
    # Initialize a new numpy array
    new_nd_array = np.ndarray(shape=(1, 2, z_dim, img.dims.Y, img.dims.X))
    
    print("NEW ARRAY INITIALIZED -- " + str(datetime.now()))

    # for every z stack of the old file (in z stack range)
    # take channel 0 and channel 2 and put them in the new image array (channels 0 and 1)
    for z in range(0, z_dim):
        new_nd_array[0][0][z] = img.data[0][0][z + actual_range_start]
        new_nd_array[0][1][z] = img.data[0][2][z + actual_range_start]

    # Construct a new AICSImage object
    new_img = AICSImage(new_nd_array, physical_pixel_sizes=img.physical_pixel_sizes)
    
    print("NEW AICSImage CONSTRUCTED -- " + str(datetime.now()))
    
    filename = str(filepath).rsplit('/', 1)[1]
    savepath = str(filepath).rsplit('/', 2)[0] + '/subset_ometiffs/'
    
    # print(savepath +  str(filename).split('.')[0] + '_subset.ome.tiff')
    new_img.save(savepath + str(filename).split('.')[0] + '_subset.ome.tiff')
    
    print("NEW OME-TIFF FILE SAVED -- " + str(datetime.now()))
    print(savepath)
    print(filename)

# Where range_params.txt is a tab-sep file of the absolute path of the original OME-TIFF and range of the slices to take
# e.g.: `/path/to/my/imaging_file.ome.tiff  25  100`
with open("range_params.txt") as param_file:
    # next(param_file)
    for line in param_file:

        print(line)

        czi = line.split('\t')[0]
        start = int(line.split('\t')[1])
        end = int(line.split('\t')[2])

        print(czi)
        print(start)
        print(end)
        
        # Get start time for timer
        begin = datetime.now()
        print("Processing START time:", begin)

        # Main function
        subsetczi_writeometiff(czi, int(start), int(end))

        # Print current data and time (AFTER main fn)
        finish = datetime.now()
        print("Processing END time:", finish)
