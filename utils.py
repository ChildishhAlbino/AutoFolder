import json
import shutil
from shutil import copyfile, rmtree
import subprocess
from os import remove, rename, walk, mkdir
from os.path import exists, isfile
from pathlib import Path
from zipfile import ZipFile
from PIL import Image
import ffmpy
from send2trash.plat_win import send2trash


def inFileMask(filePath, fileMask, globalFileMasks):
    if(fileMask == None):
        return True
    p = Path(filePath)
    return p.suffix in getFileMask(fileMask, globalFileMasks)


def getFileMask(fileMask, globalFileMasks):
    t = type(fileMask)
    if(t is list):
        return fileMask
    elif(t is str):
        val = globalFileMasks[fileMask]
        return val
    else:
        print("Invalid File Mask")
        return []


def convert(inputPath, mimeType, globalOptions, inputOptions, outputOptions):
    inputSuffix = Path(inputPath).suffix
    convertedFileName = inputPath.replace(
        "%s" % (inputSuffix), ".%s" % (mimeType))
    duplicateCount = 1
    while(exists(convertedFileName)):
        convertedFileName = inputPath.replace(
            "%s" % (inputSuffix), "-%s.%s" % (duplicateCount, mimeType))
        duplicateCount = duplicateCount + 1
    convert = ffmpy.FFmpeg(
        global_options=globalOptions,
        inputs={inputPath: inputOptions},
        outputs={convertedFileName: outputOptions}
    )
    print("")
    convert.run()


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
        print(e)
    if (deleteArchive):
        remove(archivePath)


def rename(filePath, newFileName):
    print("rename")
    rename(filePath, newFileName)


def delete(filePath):
    print("delete")
    if (isfile(filePath)):
        remove(filePath)
    else:
        shutil.rmtree(filePath)


def copy(startingFolder, destinationFolder, files, deleteSourceFile):
    dirs = [x[0]
            for x in walk(startingFolder) if x[0] != startingFolder]
    for dir in dirs:
        replacedDir = dir.replace(startingFolder, destinationFolder)
        if(not exists(replacedDir)):
            mkdir(replacedDir)

    for file in files:
        copyfile(file, file.replace(startingFolder, destinationFolder))

    if(deleteSourceFile):
        for dir in dirs:
            rmtree(dir)

        for file in files:
            try:
                send2trash(file)
            except:
                remove(file)


def getVideoDuration(videoPath):
    print(videoPath)
    metaData = ffmpy.FFprobe(
        inputs={videoPath: None},
        global_options=[
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format', '-show_streams']
    ).run(stdout=subprocess.PIPE)
    meta = json.loads(metaData[0].decode('utf-8'))
    duration = meta["streams"][0]["duration"]
    duration = round(float(duration), 0)
    return duration


def getImageResolution(imagePath):
    try:
        # uses PIL to get image size.
        img = Image.open(imagePath)
        h, w = img.size
        dimensions = [h, w]
        return dimensions
    except Exception as e:
        print(e)
