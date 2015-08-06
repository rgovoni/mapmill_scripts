import os, shutil, sys

# usage: cluster.py [image_folder] [feat_folder] [set_size] [s or d]
folder = sys.argv[1]
folder_feat = sys.argv[2]
setsize = int(sys.argv[3])
similar = {'s':True, 'd':False}[sys.argv[4]]


# find images in folder
imagenames = [name for name in os.listdir(folder) if name.endswith('.jpg')]
imagenames = sorted(imagenames)

# load in features
feats = []
for imagename in imagenames:
    infile = open(folder_feat + '/' + imagename + '.feat')
    feats.append([float(x) for x in infile.xreadlines()])
    infile.close()


# compute all pairwise distances
print 'computing distance matrix...'
dists = {}
for ii in xrange(len(feats)):
    for jj in xrange(ii + 1, len(feats)):

        dist = 0.0
        for (aa, bb) in zip(feats[ii], feats[jj]):
            dist += (aa - bb) ** 2
        dist = dist ** 0.5

        dists[(ii, jj)] = dist
        dists[(jj, ii)] = dist


# compute initial strange points
print 'computing strange points...'
max_dist = -1.0
strange_points = None
for ii in xrange(len(feats)):
    for jj in xrange(ii + 1, len(feats)):
        this_dist = dists[(ii, jj)]
        if this_dist > max_dist:
            max_dist = this_dist
            strange_points = [ii, jj]

# compute remaining strange points
if not similar:
    while len(strange_points) < setsize:
        print len(strange_points)

        max_dist = -1.0
        max_point = None
        for ii in xrange(len(feats)):
            if ii in strange_points:
                continue
        
            curr_dist = 0.0
            for jj in strange_points:
                curr_dist += dists[(ii, jj)]

            if curr_dist > max_dist:
                max_dist = curr_dist
                max_point = ii

        strange_points.append(max_point)

# compute sets
    print 'computing sets...'
    sets = []
    for sp in strange_points:
        sets.append([imagenames[sp]])

else:
    sets = [[strange_points[0]], [strange_points[1]]]
    set_dist = [0.0, 0.0]

    for ss in xrange(2):
        while len(sets[ss]) < setsize:
            min_dist = 1e100
            min_point = None
            for ii in xrange(len(feats)):
                if ii in sets[0] or ii in sets[1]:
                    continue

                curr_dist = dists[(strange_points[ss], ii)]

                if curr_dist < min_dist:
                    min_dist = curr_dist
                    min_point = ii

            sets[ss].append(min_point)
            set_dist[ss] += min_dist

    if set_dist[0] < set_dist[1]:
        del sets[1]
        del set_dist[1]
    else:
        del sets[0]
        del set_dist[0]

    sets[0] = [imagenames[ii] for ii in sets[0]]

# remove old output folder
print 'copying images...'
out = 'img_set'
shutil.rmtree(out, True)


# copy to output folder
for si, set in enumerate(sets):
    outfolder = out + '/s%03d' % si
    os.makedirs(outfolder)
    for ss in set:
        shutil.copyfile(folder + '/' + ss, outfolder + '/' + ss)


# make index
outfile = open(out + '/index.html', 'w')

outfile.write('<html>\n')
outfile.write('<head></head>\n')
outfile.write('<body>\n')
for dd in sorted(os.listdir(out)):
    if os.path.isdir(out + '/' + dd):
        for ff in os.listdir(out + '/' + dd):
            outfile.write('<img src=' + dd + '/' + ff + '>\n')
        outfile.write('<!-- -->\n')
        #outfile.write('<hr>\n')
outfile.write('</body>\n')
outfile.write('</html>\n')
