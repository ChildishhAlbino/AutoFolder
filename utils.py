import ffmpy
import subprocess
import json
from zipfile import ZipFile
from os import listdir, remove
from os.path import isfile, join, exists
from pathlib import Path


def convert(inputPath, mimeType, convertType, inputOption, outputOptions):
    print("convert")
    # check convert type, if convert type is video to image, do that.
    # else, do that.


def unzip(archivePath, deleteArchive, nested):
    print("unzip")

    path = Path(archivePath)
    parentPath = path.parent

    absoluteArchivePath = str(path.absolute())
    absoluteParentPath = str(parentPath.absolute())
    if (nested):
        absoluteParentPath = str(Path(absoluteParentPath).joinpath(path.stem))
    try:
        with ZipFile(absoluteArchivePath) as zipped:
            zipped.extractall(path=absoluteParentPath)
    except Exception as e:
        # If a zipfile requires a password, the zipfile won't be extracted.
        # File will then be copied in zipped fashion.
        print(e)
    if (deleteArchive):
        remove(archivePath)


def rename(filePath, newFileName, deleteOldFile):
    print("rename")


def delete(filePath, recycle):
    print("delete")
