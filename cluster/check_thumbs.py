# script to check that CAP server thumbnail images have corresponding high-resolution images

import os, sys, shutil, urllib2

# usage: check_thumbs.py [image_folder]
folder = sys.argv[1]

# find images in folder
imagenames = [name for name in os.listdir(folder) if name.endswith('.jpg')]

# remove old output folder
outfolder = folder + '_check'
shutil.rmtree(outfolder, True)
os.makedirs(outfolder)

# go through all the images
for ii, imagename in enumerate(imagenames):
    print ii + 1, '/', len(imagenames),

    # check full resolution image exists on server
    url = 'http://dev.femadata.com/capuploadhandler/files/22/' + imagename.replace('.thumbnail', '')
    try:
        urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print 'missing', imagename
        continue
    except urllib2.URLError, e:
        print 'missing', imagename
        continue

    # copy file
    print 'copying', imagename
    shutil.copyfile(folder + '/' + imagename, outfolder + '/' + imagename)
