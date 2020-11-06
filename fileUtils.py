from os import walk, scandir
from os.path import isdir


def getFiles(directory):
    dirs = [x[0] for x in walk(directory)]
    files = []
    for dir in dirs:
        newFiles = [file.path for file in scandir(dir)]
        files.extend([file for file in newFiles if isdir(file) == False])
    return files
