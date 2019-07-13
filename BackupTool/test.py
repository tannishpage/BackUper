"""
Define Backup:
    - To store a copy of a personal files from a system in a safe reliable place
    - Personal files include Music, Documents, Videos, Pictures

Backup Procedure:
    1. Compress the following folders
        - Music
        - Documents
        - Videos
        - Pictures
    2. Add the above compressed "zip" files to a single compressed zip file
    3. Name this master zip file with the date and time the back up happens
    4. Move the master zip to the backup folder in primary back up.
    5. Quit

Automated backup:
    - Impliment later
"""

import os
import sys
import shutil
import datetime
date = "".join(str(datetime.datetime.now()).split(" ")[0].split("-"))
time = "".join(str(datetime.datetime.now()).split(" ")[1].split(".")[0].split(":"))
def initializing():
    sys.stdout.write("\rInitiating...")
    os.chdir("/home/tannishpage")
    os.mkdir("PCBackup-{}-{}".format(date, time))
    os.chdir("PCBackup-{}-{}".format(date, time))
    sys.stdout.write("\rInitiating...Done\n")
    sys.stdout.write("\rStarting Zipping process\n")
    zipping()

def Cp(fname, destination, sorting_dir):
    fileOriginal = open(fname, "rb")
    os.chdir(destination) #In this case destination is a full path.
    fileDuplicate = open(fname, "wb")
    fileOriginal.seek(0, 2)
    tsize = fileOriginal.tell()
    fileOriginal.seek(0,0)
    percent = 0
    size = 0
    while True:
        data = fileOriginal.read(8192)
        if not data:
            break
        fileDuplicate.write(data)
        size = size + len(data)
        percent = 100 * (size/tsize)
        sys.stdout.write("\r[{0}{1}] {2:.3f}% ".format('='*int(percent/10), '.'*(10-int(percent/10)), percent))
    fileOriginal.close()
    fileDuplicate.close()
    os.chdir(sorting_dir)
    os.remove(fname)

def zipping():
    dir_names = ['/home/tannishpage/Music', '/home/tannishpage/Documents', '/home/tannishpage/Videos', '/home/tannishpage/Pictures']
    for dir_name in dir_names:
        sys.stdout.write("\rZipping {}...".format(dir_name.split("/")[3]))
        shutil.make_archive(dir_name.split("/")[3], "zip", dir_name) #This will create a zip file of the directory dir_name
        sys.stdout.write("\rZipping {}...Done\n".format(dir_name.split("/")[3]))
    else:
        sys.stdout.write("\rZipping all zips into one file...")
        os.chdir("..")
        shutil.make_archive("PCBackup-{}-{}".format(date, time), "zip", "PCBackup-{}-{}".format(date, time))
        sys.stdout.write("\rZipping all zips into one file...Done\n")
        sys.stdout.write("\rCopying Files to backup folder\n")
        Cp("PCBackup-{}-{}.zip".format(date, time), "/media/tannishpage/PrimaryBackUpDisk/BackUps", "/home/tannishpage")
        sys.stdout.write("\r\nBackup Process has successfully completed. Exiting.\n")

initializing()
        
