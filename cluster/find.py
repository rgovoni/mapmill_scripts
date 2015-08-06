# script to clean out irregular images

import hashlib, os, sys, shutil
from PIL import Image, ImageChops

# usage: find.py [image] [image_folder]
filename = sys.argv[1]
folder = sys.argv[2]

# find images in folder
imagenames = [name for name in os.listdir(folder) if name.endswith('.jpg')]

# open find image
find = Image.open(filename)
find = find.convert('L')
closest_img = None
closest_dist = 1e100

# go through all the images
for ii, imagename in enumerate(imagenames):
    print ii + 1, '/', len(imagenames),
    fullname = folder + '/' + imagename

    # load image
    im = Image.open(fullname)
    im = im.convert('L')

    # compare
    find_resized = find.resize(im.size)
    im_diff = ImageChops.difference(im, find_resized)
    diff_data = im_diff.getdata()
    diff = reduce(lambda x, y: x + y ** 2.0, diff_data, 0)
    diff = float(diff) / len(diff_data)
    print diff, closest_dist, closest_img
    if diff < closest_dist:
        closest_dist = diff
        closest_img = imagename

print closest_img, closest_dist
