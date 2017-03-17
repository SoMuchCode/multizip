#!/usr/bin/env python
#
# multizip.py
# version 0.3
# perform zip operations on multiple files and/or multiple folders.
# Python 3.6
# CLM 20170117
#
# USAGE: multizip.py /path/to/files/you/want/to/compress/ /optional/output/dir/
# By default output files will be created in directory where multizip is invoked.

try:
    from distutils.archive_util import zipfile
    import sys, os
except ImportError:
    print('Exception: cannot load module')
    print('Exiting...')
    sys.exit(-1)

verb = 0
argcount = 0
zipp_path = ''
filentmp = ''
outputpath = ''
win = 0
if os.name == 'nt':
    win = 1

def make_zipfile(base_name, base_dir):
    zip_filename = os.path.join(outputpath, base_name) + ".zip"
    zip_path = os.path.join(base_dir, base_name)
    # are we doing a file or a dir?
    if (verb > 0):
        print('base name:',base_name)
        print('base dir:',base_dir)
        print('zip_filename:',zip_filename)
        print('zip_path:',zip_path)
    if os.path.isdir(zip_path):     # for a dir
        if (verb > 0):
            print('dir')
        zf = zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED)
        for folderName, subfolders, filenames in os.walk(zip_path):
            if verb>0:
                print('The current folder is ' + folderName)
            for subfolder in subfolders:
                if verb>0:
                    print('SUBFOLDER OF ' + folderName + ': ' + subfolder)
            for filename in filenames:
                print('Compressing: ' + folderName + ' '+ filename)
                zipp_path = folderName.split(base_dir)
                zp = zipp_path[1]
                filentmp = os.path.join(zp,filename)
                zp = os.path.join(folderName,filename)
                zf.write(zp, filentmp)
        zf.close()

    else:       # for a file
        if verb>0:
            print('file')
        print('Compressing: ' + zip_path)
        zf = zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED)
        zf.write(zip_path, base_name)
        zf.close()

def help():
    print('USAGE:')
    if win == 1:
        print(sys.argv[0],'C:\\path\\to\\files\\you\\want\\to\\compress\\ \\optional\\output\\dir\\')
    else:
        print(sys.argv[0],'/path/to/files/you/want/to/compress/ /optional/output/dir/')
    exit()

# count arguments
for arg in sys.argv:
    argcount += 1
    if (arg == '--h' or arg == '-h' or arg == '--help' or arg == '/h' or arg == '/?'):
        help()

if (argcount < 2 or argcount > 3):
    print('ERROR: You need to supply a path')
    help()

if argcount == 3:
    outputpath = os.path.abspath(sys.argv[2])
    if verb > 0:
        print(outputpath)

if not os.path.isdir(sys.argv[1]):
    print('ERROR: I need a directory path, not a file path')
    help()

if verb>0:
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv),'\n')

pathname = os.path.abspath(sys.argv[1])
if verb>0:
    print('path:',pathname)
    os.listdir(pathname)

for ii in os.listdir(pathname):
    if verb>0:
        print('file or folder:',ii)
    make_zipfile(ii,pathname)

