import csv
import os

PATH = r"E:.\朗文直排\sent_rename\sent_rename"

with open('data.csv','w',newline='',encoding='utf-8') as f:
    w = csv.writer(f)

    # Write a header row
    w.writerow('foldername filename'.split())

    # path is the current directory being walked.
    # dirs is a list of the directories in this path.  It can be edited to skip directories.
    # files is a list of files in this path.
    i=1
    for path,dirs,files in os.walk(PATH):
        for file in files:
            # Join the path to the current file.
            current = os.path.join(path,file)
            # Remove the root path.
            # Split the remaining "Interpret\Album\Title" into a list.
            row = os.path.relpath(current,PATH).split(os.sep)
            w.writerow(row)
            
