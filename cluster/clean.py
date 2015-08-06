# script to clean out irregular images

import hashlib, os, sys, shutil
from PIL import Image

TO_REMOVE = [
    'b08c6bcb-12a9-4506-a69c-1c98f78ff466',
    '1a8c809d-b418-4306-b28f-bf85738b8297',
    '1a601831-e9e8-47d0-ad64-fc8564866aa8',
    '00f97031-950a-4174-bd45-71882ff33ff3',
    '01f261e9-86fa-444f-abc2-e4bdff2f3641',
    '1a0a0a6f-69b0-4a35-82f1-673a97037b3d',
    '01a35317-e591-4371-8627-5a521d4a86f8',
    '01e82904-1fe2-4ed7-b69d-077c674b812d',
    '1a350e50-3115-4e5f-ade3-0c4355299563',
]

# usage: clean.py [image_folder]
folder = sys.argv[1]

# find images in folder
imagenames = [name for name in os.listdir(folder) if name.endswith('.jpg')]

# remember seen images
seen_hash = {}

# remove old output folder
outfolder = folder + '_clean'
shutil.rmtree(outfolder, True)
os.makedirs(outfolder)

# go through all the images
for imagename in imagenames:
    # get imagename
    fullname = folder + '/' + imagename

    # load image
    im = Image.open(fullname)

    # check for duplicates
    hash = hashlib.md5(im.tostring()).hexdigest()
    if seen_hash.has_key(hash):
        print 'duplicate hash ' + hash
        continue
    
    # remember image hash
    seen_hash[hash] = True

    # check bands
    if im.getbands() != ('R', 'G', 'B'):
        print 'unrecognized bands ' + ''.join(im.getbands())
        continue

    # check aspect ratio
    #if im.size[1] > im.size[0]:
    if im.size[0] != 256 or im.size[1] not in [170, 171]:
        print 'bad aspect ratio'
        continue

    # check for some colors
    if im.getextrema() == ((0, 0), (0, 0), (0, 0)):
        print 'no colors'
        continue

    # remove specific images
    found = False
    for rem in TO_REMOVE:
        if imagename.startswith(rem):
            found = True

    if found:
        print 'skipping specific image ' + imagename
        continue

    # copy file
    shutil.copyfile(folder + '/' + imagename, outfolder + '/' + imagename)
