import colorsys, os, shutil, sys
from PIL import Image

HUE_BUCKETS = 16
SAT_BUCKETS = 4
VAL_BUCKETS = 4

# usage: cluster.py [image_folder]
folder = sys.argv[1]

# find images in folder
imagenames = [name for name in os.listdir(folder) if name.endswith('.jpg')]

# remove old output folder
outfolder = folder + '_feat'
shutil.rmtree(outfolder, True)
os.makedirs(outfolder)

# go through all the images
for ii, imagename in enumerate(imagenames):
    print ii + 1, '/', len(imagenames), imagename

    # load image
    im = Image.open(folder + '/' + imagename)

    #initialize buckets
    buckets = [0] * (HUE_BUCKETS * SAT_BUCKETS * VAL_BUCKETS)
    count = 0

    # go through all the colors
    clr = im.getcolors(im.size[0] * im.size[1])
    for cn, (rr, gg, bb) in clr:
        # convert to hsv
        hh, ss, vv = colorsys.rgb_to_hsv(rr/255., gg/255., bb/255.)

        # figure out the bucket
        hb = int(hh * HUE_BUCKETS) % HUE_BUCKETS
        sb = min(int(ss * SAT_BUCKETS), SAT_BUCKETS - 1)
        vb = min(int(vv * VAL_BUCKETS), VAL_BUCKETS - 1)

        # update bucket
        buckets[hb * SAT_BUCKETS * VAL_BUCKETS + sb * VAL_BUCKETS + vb] += cn
        count += cn

    # accumulate buckets
    for ii in xrange(1, len(buckets)):
        buckets[ii] += buckets[ii - 1]

    # normalize buckets
    output = map(lambda x:float(x)/count, buckets)

    # save features
    outname = outfolder + '/' + imagename + '.feat'
    outfile = open(outname, 'w')
    for num in output:
        outfile.write(str(num) + '\n')
    outfile.close()
