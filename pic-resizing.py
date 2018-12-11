"""
A script designed to  1) resize all of the downloaded images to desired dimension 
(DEFAULT 512x512) and 2) name images from 1.png to n.png for ease of use in training
"""

import os
import skimage
from skimage.io import imread, imsave
from skimage.transform import resize
import random
import re

from multiprocessing import Pool


root= '/home/gengroup/metcontainer/PrimaryImage'   #source images
target= '/home/gengroup/resized-images'
n = 0

def makeImage(f):
    match = re.search('^[^0-9]*([0-9]*)_1.jpg', f)
    if match : i = match.group(1) 
    else: return  # if not a suitable filename, next

    saveto = target + '/' + str(i) + '.png'
    if os.path.isfile(saveto): return  # don't waste effort

    ffull = root + '/' + f
    size = os.path.getsize(ffull)
    if size < 2000: return   # ignore failed downloads
    print(i , f)             # progress check 
    try:
        image  = imread(ffull)
        image2 = resize(image,(512,512), mode='reflect', anti_aliasing=True)
        imsave(saveto, image2)
        n += 1
    except Exception:
        print('missed it: ' + f)

pool = Pool(10)
for root, dirs, files in os.walk(root):  # anything faster than walk? 
    pool.map(makeImage, files)

print('Done! ' + str(n))  # n is the # of files written

# add image to array (separate fxn)
