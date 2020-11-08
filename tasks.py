# These are the actual functions that will be run by the AF Engine to transform files.
# They handle validation logic and extract boiler plate from the actual utility functions.
from os import pipe
from typing import Collection
from utils import convert, rename, unzip, delete, copy
from iterators import getIteratorData
from dataUtils import createKwargs
from concurrent.futures import ThreadPoolExecutor


def TASK_convert(pipelineData, arguments, iteratorConfig):
    length = len(pipelineData)
    with ThreadPoolExecutor() as executor:
        executor.map(WRAP_MT(
            arguments, iteratorConfig, MT_convert, pipelineData, length), pipelineData, length)


def WRAP_MT(arguments, iteratorConfig, f, collection, length):
    return lambda filePath: LOG_MT(filePath, arguments, iteratorConfig, f, collection, length)


def LOG_MT(filePath, arguments, iteratorConfig, f, collection, length):
    itemNo = collection.index(filePath) + 1
    print("Item #%s of %s starting!\n" % (itemNo, length))
    return f(filePath, arguments, iteratorConfig)


def MT_convert(filePath, arguments, iteratorConfig):
    # if iterator, generator iterator response.
    if(iteratorConfig):
        iterationData = getIteratorData(iteratorConfig, filePath)

        kwargsArray = [createKwargs(arguments, filePath, iteration)
                       for iteration in iterationData]

        print("Iterator detected! Converting file into %s files!" %
              (len(kwargsArray)))

        for index, kwargs in enumerate(kwargsArray):
            print("Iterating... %s / %s\n" % (index + 1, len(kwargsArray)))
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
    for index, file in enumerate(pipelineData):
        print("Deleting... %s / %s" % (index + 1, len(pipelineData)))
        arguments["filePath"] = file
        delete(**arguments)


def TASK_copy(pipelineData, arguments, iteratorConfig):
    arguments["files"] = pipelineData
    copy(**arguments)
