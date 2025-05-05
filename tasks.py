# These are the actual functions that will be run by the AF Engine to transform files.
# They handle validation logic and extract boiler plate from the actual utility functions.
from utils import convert, rename, unzip, delete, copy, logMTCall
from fileUtils import getFiles
from iterators import getIteratorData
from dataUtils import createKwargs
from concurrent.futures import ThreadPoolExecutor
from utils import getCopyArguments, isDryRun
from os import remove, rename, walk, mkdir, utime
from os.path import exists, isfile, getctime, getmtime
from shutil import copyfile, rmtree
from pathlib import Path
import re


def TASK_convert(pipelineData, arguments, iteratorConfig, isDryRun):
    length = len(pipelineData)
    maxWorkers = arguments.get('maxWorkers')
    with ThreadPoolExecutor(max_workers=maxWorkers) as executor:
        executor.map(HANDLE_MT(
            arguments, iteratorConfig, MT_convert, pipelineData, length, "Converting Item #%s of %s", isDryRun), pipelineData)


def HANDLE_MT(arguments, iteratorConfig, f, collection, length, overrideText=None, isDryRun=False):
    return lambda filePath: logMTCall(filePath, arguments, iteratorConfig, f, collection, length, overrideText, isDryRun)


def MT_convert(filePath, arguments, iteratorConfig, isDryRun):
    # if iterator, generator iterator response.
    if(iteratorConfig):
        iterationData = getIteratorData(iteratorConfig, filePath)
        kwargsArray = [createKwargs(arguments, filePath, iteration)
                       for iteration in iterationData]
        print("Iterator detected! Converting file %s into %s files!" %
              (filePath, len(kwargsArray)))

        for index, kwargs in enumerate(kwargsArray):
            print("Iterating... %s / %s" %
                  (index + 1, len(kwargsArray)))
            if not isDryRun:
                convert(**kwargs)
            else:
                print(f"Would iteratively convert: {filePath}")
    else:
        arguments["inputPath"] = filePath
        if not isDryRun:
            convert(**arguments)
        else:
            print(f"Would convert: {filePath}")


def TASK_rename(pipelineData, arguments, iteratorConfig, isDryRun):
    new_file_name_arg = arguments.get("newFileName", None)
    is_regex = arguments.get("regex", False)
    replacer = arguments.get("replacer", None)
    for file in pipelineData:
        new_file_name = new_file_name_arg
        path = Path(file)
        parent_path = path.parent
        file_name = path.name
        print(file_name)
        new_file_name = new_file_name_arg
        if(is_regex is True):
            if(replacer is not None):
                new_file_name = re.sub(
                    new_file_name_arg, replacer, file_name)
            else:
                new_file_name = re.search(new_file_name_arg, file_name)[0]
        print(new_file_name)
        if(new_file_name is not None):
            new_file_path = "%s/%s" % (parent_path, new_file_name)
            if not isDryRun:
                rename(file, new_file_path)
            else:
                print(f"Would rename: {file} to {new_file_path}")


def TASK_unzip(pipelineData, arguments, iteratorConfig, isDryRun):
    for index, file in enumerate(pipelineData):
        print("Converting... %s / %s" % (index + 1, len(pipelineData)))
        arguments["archivePath"] = file
        if not isDryRun:
            unzip(**arguments)
        else:
            print(f"Would unzip: {file}")


def TASK_delete(pipelineData, arguments, iteratorConfig, isDryRun):
    length = len(pipelineData)
    with ThreadPoolExecutor() as executor:
        executor.map(HANDLE_MT(
            arguments, iteratorConfig, MT_delete, pipelineData, length, "Deleting Item #%s of %s", isDryRun), pipelineData)


def MT_delete(filePath, arguments, iteratorConfig, isDryRun):
    if not isDryRun:
        delete(filePath)
    else:
        print(f"Would delete: {filePath}")


def TASK_copy(pipelineData, arguments, iteratorConfig, isDryRun):
    (startingFolder, destinationFolder,
     deleteOriginalFiles) = getCopyArguments(arguments)

    if(not exists(destinationFolder)):
        print("Created destination directory.")
        mkdir(destinationFolder)

    dirs = [x[0]
            for x in walk(startingFolder) if x[0] != startingFolder]
    # print("Recreating Directory Structure\n")
    length = len(pipelineData)
    with ThreadPoolExecutor() as executor:
        executor.map(HANDLE_MT(
            arguments, iteratorConfig, MT_copy, pipelineData, length, "Copying Item #%s of %s", isDryRun), pipelineData)
    if not isDryRun:
        deleteSourceDirectory(pipelineData, arguments,
                              iteratorConfig, deleteOriginalFiles, dirs)


def deleteSourceDirectory(pipelineData, arguments, iteratorConfig, deleteOriginalFiles, dirs):
    if(deleteOriginalFiles and len(pipelineData) > 0):
        print("Deleting original copied of filtered files...")
        TASK_delete(pipelineData, arguments, iteratorConfig, False)
     
def MT_copy(filePath, arguments, iteratorConfig, isDryRun):
    (startingFolder, destinationFolder,
     deleteSourceFile) = getCopyArguments(arguments)
    destinationPath = filePath.replace(startingFolder, destinationFolder)
    if not isDryRun:
        copy(filePath, destinationPath)
        ctime = getctime(filePath)
        mtime = getmtime(filePath)
        utime(destinationPath, (ctime, mtime))
    else:
        print(f"Would copy: {filePath}")
