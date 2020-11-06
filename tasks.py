# These are the actual functions that will be run by the AF Engine to transform files.
# They handle validation logic and extract boiler plate from the actual utility functions.
from utils import convert, rename, unzip, delete, copy
from iterators import getIteratorData
from dataUtils import createKwargs


def TASK_convert(pipelineData, arguments, iteratorConfig):
    print("Converting %s files!" % (len(pipelineData)))
    for index, file in enumerate(pipelineData):
        print("Converting... %s / %s" % (index + 1, len(pipelineData)))
        # if iterator, generator iterator response.
        if(iteratorConfig):
            iterationData = getIteratorData(iteratorConfig, file)

            kwargsArray = [createKwargs(arguments, file, iteration)
                           for iteration in iterationData]

            print("\nIterator detected! Converting file into %s files!" %
                  (len(kwargsArray)))

            for index, kwargs in enumerate(kwargsArray):
                print("\nIterating... %s / %s" % (index + 1, len(kwargsArray)))
                convert(**kwargs)
        else:
            arguments["inputPath"] = file
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
        arguments["filePath"] = file
        delete(**arguments)


def TASK_copy(pipelineData, arguments, iteratorConfig):
    arguments["files"] = pipelineData
    copy(**arguments)
