import sys, os

# usage: make_page.py [output_folder]
folder = sys.argv[1]

outfile = open(folder + '/index.html', 'w')

outfile.write('<html>\n')
outfile.write('<head></head>\n')
outfile.write('<body>\n')
for dd in sorted(os.listdir(folder)):
    if os.path.isdir(folder + '/' + dd):
        for ff in os.listdir(folder + '/' + dd):
            outfile.write('<img src=' + dd + '/' + ff + '>\n')
        outfile.write('<hr>\n')
outfile.write('</body>\n')
outfile.write('</html>\n')
