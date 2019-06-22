#! /usr/bin/env python3

# GoPro Joiner - a script to automatically join video files splitted by GoPro using ffmpeg
# Author: Peter Urgoš (petak5)

#ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.mp4

import os
import sys

def getFileNumber(fileName):
    return fileName[-8] + fileName[-7] + fileName[-6] + fileName[-5]

def getFileChapter(fileName):
    return fileName[-10] + fileName[-9]

temp_list_name = '.temp_list.txt'
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

#print(fileNumbers)

if os.path.isfile(temp_list_name):
    os.remove(temp_list_name)
