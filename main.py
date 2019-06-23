#! /usr/bin/env python3

# GoPro Joiner - a script to automatically join video files splitted by GoPro using ffmpeg
# Author: Peter Urgoš (petak5)
# Dependencies: ffmpeg
# Description: This program reads file names generated by a GoPro and checks if there are any videos chaptered into multiple files. It then uses ffmpeg to join these MPEG-4 (or MP4) files. The file names cannot be modified for this script to work as expected!
# Usage: Import GoPro videos through the GoPro Quik app or manually (copy video files from the SD card). Then execute this script and pass the directory containing the imported media as a paramater. Example: `./main.py './GoPro Video Files'`. The created files are named `GX00` + <id_number> + `.MP4`
# Technical details: The script executes a command based on this template: `ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.MP4` with `mylist.txt` containing the file names to join prefixed with `file ` and one file name per line, and `output.MP4` being the joined files into one MP4.

import os
import sys

def getFileNumber(fileName):
    return fileName[-8] + fileName[-7] + fileName[-6] + fileName[-5]

def getFileChapter(fileName):
    return fileName[-10] + fileName[-9]

if len(sys.argv) != 2:
    print("Usage: `./main.py <path_to_GoPro_videos>`")

temp_list_name = '.gj_temp_list.txt'
str_directory = str(os.path.abspath(sys.argv[1])) + '/'
directory = os.fsencode(str_directory)
os.chdir(directory)

files = []

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".MP4") or filename.endswith(".mp4"):
        files.append(filename)

fileNumbers = {}
for file in files:
    number = getFileNumber(file)
    chapter = getFileChapter(file)
    
    if number not in fileNumbers:
        fileNumbers[number] = [chapter]
    else:
        fileNumbers[number].append(chapter)

# Delete items with less than 2 chapters
for key, value in list(fileNumbers.items()):
    if len(value) < 2:
        del fileNumbers[key]

for number, chapters in fileNumbers.items():
    with open(temp_list_name, 'w') as the_file:
        files = []
        for chapter in chapters:
            files.append('GX' + chapter + number + '.MP4')
        files.sort()
        for file in files:
            the_file.write('file \'' + file + '\'\n')

    os.system('ffmpeg -f concat -safe 0 -i "' + temp_list_name + '" -c copy "' + 'GX00' + number + '.MP4"')

# Delete the temporary list file if exists
if os.path.isfile(temp_list_name):
    os.remove(temp_list_name)
