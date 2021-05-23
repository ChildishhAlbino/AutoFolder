from os import walk, scandir
from os.path import isdir, getmtime


def getFiles(directory, shallow=False):
    files = []
    if(shallow):
        newFiles = [file.path for file in scandir(directory)]
        files.extend(
            [file for file in newFiles if isdir(file) == False])
    else:
        dirs = [x[0] for x in walk(directory)]
        for dir in dirs:
            newFiles = [file.path for file in scandir(dir)]
            files.extend([file for file in newFiles if isdir(file) == False])
    files = sorted(files, key=getmtime)
    return files
