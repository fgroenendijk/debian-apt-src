#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import argparse
import hashlib
import os

parser = argparse.ArgumentParser()
parser.add_argument("src", help="Source directory of package")
args = parser.parse_args()

srcDirectory = args.src

if not srcDirectory.endswith('/'):
    srcDirectory += '/'

def fileDigest(filePath, algorithm):
    h = None
    if algorithm == 'sha1':
        h = hashlib.sha1()
    elif algorithm == 'sha256':
        h = hashlib.sha256()
    else:
        h = hashlib.md5()

    with open(filePath, 'rb') as file:
        while True:
            # Reading is buffered, so we can read smaller chunks.
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()

print('Searching for control files in {}'.format(srcDirectory + 'debian/[^/]*/DEBIAN/control'))
controlFiles = glob.glob(srcDirectory + 'debian/*/DEBIAN/control')

print(glob.glob(srcDirectory))

packageFile = open("Packages", "w")

for controlFile in controlFiles:
    if not '-dbg' in controlFile:
        print('Found controlfile: {}'.format(controlFile));
        f = open(controlFile, "r")

        packageName = None

        for line in f:
            if line.startswith('Package'):
                packageName = line.replace('Package: ', '').rstrip()
            elif line.startswith('Version'):
                packageName += '_' + line.replace('Version: ', '').rstrip() + '*.deb'
                line = line.replace(version + ')', version + EXT + ')')
                line = re.sub('\\)' + EXT + '$', ')', line) + os.linesep
            elif line.startswith('Homepage: '):
                packageFile.write(line)
                line = 'Filename: pool/n/ng/' + packageName.replace('*.deb', EXT + '_amd64.deb') + os.linesep
                print('Added filename: ' + line
            elif line.startswith('Description: '):
                if packageName:
                    print(packageName)
                    debianPackages = glob.glob(packageName)
                    for debianPackage in debianPackages:
                        debianPackageDest = debianPackage.replace('_amd64.deb', '-vod_amd64.deb')
                        os.rename(debianPackage, debianPackageDest)
                        packageFile.write('SHA1: ' + fileDigest(debianPackageDest, 'sha1') + os.linesep)
                        packageFile.write('SHA256: ' + fileDigest(debianPackageDest, 'sha256') + os.linesep)
                        packageFile.write('MD5sum: ' + fileDigest(debianPackageDest, 'md5') + os.linesep)

            packageFile.write(line)

        packageFile.write(os.linesep)

