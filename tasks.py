# These are the actual functions that will be run by the AF Engine to transform files.
# They handle validation logic and extract boiler plate from the actual utility functions.
from utils import convert, rename, unzip, delete, copy
from iterators import getIteratorData
from dataUtils import createKwargs
from concurrent.futures import ThreadPoolExecutor


def TASK_convert(pipelineData, arguments, iteratorConfig):
    length = len(pipelineData)
    with ThreadPoolExecutor() as executor:
        executor.map(HANDLE_MT(
            arguments, iteratorConfig, MT_convert, pipelineData, length), pipelineData)


def HANDLE_MT(arguments, iteratorConfig, f, collection, length):
    return lambda filePath: logMTCall(filePath, arguments, iteratorConfig, f, collection, length)

    # def handleMtFilter(fieldValue, collection, length):
    #     return lambda filePath: logMTFilter(filePath, fieldValue, collection, length)

    # def logMTFilter(filePath, fieldValue, collection, length):
    #     logFiltered(collection.index(filePath), filePath, collection)
    #     return fieldValue(filePath)


def logMTCall(filePath, arguments, iteratorConfig, f, collection, length):
    itemNo = collection.index(filePath) + 1
    print("Item #%s of %s starting!" % (itemNo, length))
    f(filePath, arguments, iteratorConfig)


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
    for index, file in enumerate(pipelineData):
        print("Deleting... %s / %s" % (index + 1, len(pipelineData)))
        arguments["filePath"] = file
        delete(**arguments)


def TASK_copy(pipelineData, arguments, iteratorConfig):
    arguments["files"] = pipelineData
    copy(**arguments)
