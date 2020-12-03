# These are the actual functions that will be run by the AF Engine to transform files.
# They handle validation logic and extract boiler plate from the actual utility functions.
from utils import convert, rename, unzip, delete, copy, logMTCall
from iterators import getIteratorData
from dataUtils import createKwargs
from concurrent.futures import ThreadPoolExecutor
from utils import getCopyArguments
from os import remove, rename, walk, mkdir
from os.path import exists, isfile
from shutil import copyfile, rmtree


def TASK_convert(pipelineData, arguments, iteratorConfig):
    length = len(pipelineData)
    with ThreadPoolExecutor() as executor:
        executor.map(HANDLE_MT(
            arguments, iteratorConfig, MT_convert, pipelineData, length, "Converting Item #%s of %s"), pipelineData)


def HANDLE_MT(arguments, iteratorConfig, f, collection, length, overrideText=None):
    return lambda filePath: logMTCall(filePath, arguments, iteratorConfig, f, collection, length, overrideText)


def MT_convert(filePath, arguments, iteratorConfig):
    # if iterator, generator iterator response.
    if(iteratorConfig):
        iterationData = getIteratorData(iteratorConfig, filePath)

        kwargsArray = [createKwargs(arguments, filePath, iteration)
                       for iteration in iterationData]

        print("Iterator detected! Converting file into %s files!" %
              (len(kwargsArray)))

        for index, kwargs in enumerate(kwargsArray):
            print("Iterating... %s / %s" % (index + 1, len(kwargsArray)))
            convert(**kwargs)
    else:
        arguments["inputPath"] = filePath
        convert(**arguments)


def TASK_rename(pipelineData, arguments, iteratorConfig):
    for file in pipelineData:
        rename(file, arguments["newFileName"])


def TASK_unzip(pipelineData, arguments, iteratorConfig):
    for index, file in enumerate(pipelineData):
        print("Converting... %s / %s" % (index + 1, len(pipelineData)))
        arguments["archivePath"] = file
        unzip(**arguments)


def TASK_delete(pipelineData, arguments, iteratorConfig):
    length = len(pipelineData)
    with ThreadPoolExecutor() as executor:
        executor.map(HANDLE_MT(
            arguments, iteratorConfig, MT_delete, pipelineData, length, "Deleting Item #%s of %s"), pipelineData)


def MT_delete(filePath, arguments, iteratorConfig):
    delete(filePath)


def TASK_copy(pipelineData, arguments, iteratorConfig):
    (startingFolder, destinationFolder,
     deleteSourceFile) = getCopyArguments(arguments)

    dirs = [x[0]
            for x in walk(startingFolder) if x[0] != startingFolder]
    print("Recreating Directory Structure\n")

    if(not exists(destinationFolder)):
        print("Created destination directory.")
        mkdir(destinationFolder)

    for index, dir in enumerate(dirs):
        print("Creating directory %s / %s" % (index + 1, len(dirs)))
        replacedDir = dir.replace(startingFolder, destinationFolder)
        if(not exists(replacedDir)):
            mkdir(replacedDir)

    length = len(pipelineData)
    with ThreadPoolExecutor() as executor:
        executor.map(HANDLE_MT(
            arguments, iteratorConfig, MT_copy, pipelineData, length, "Copying Item #%s of %s"), pipelineData)

    if(deleteSourceFile):
        print("Deleting contents of source directory.")
        TASK_delete(dirs, arguments, iteratorConfig)

        TASK_delete(pipelineData, arguments, iteratorConfig)


def MT_copy(filePath, arguments, iteratorConfig):
    (startingFolder, destinationFolder,
     deleteSourceFile) = getCopyArguments(arguments)
    destinationPath = filePath.replace(startingFolder, destinationFolder)
    copy(filePath, destinationPath)
