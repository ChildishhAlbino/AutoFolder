# These are the actual functions that will be run by the AF Engine to transform files.
# They handle validation logic and extract boiler plate from the actual utility functions.
from utils import convert, rename, unzip, delete, copy
from iterators import getIteratorData
from dataUtils import createKwargs


def TASK_convert(pipelineData, arguments, iteratorConfig):
    for index, file in enumerate(pipelineData):
        print("Converting... %s / %s" % (index + 1, len(pipelineData)))
        # if iterator, generator iterator response.
        if(iteratorConfig):
            iterationData = getIteratorData(iteratorConfig, file)

            kwargsArray = [createKwargs(arguments, file, iteration)
                           for iteration in iterationData]

            print("Iterator detected! Converting file into %s files!" %
                  (len(kwargsArray)))

            for index, kwargs in enumerate(kwargsArray):
                print("Iterating... %s / %s" % (index + 1, len(kwargsArray)))
                convert(**kwargs)
                print()
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
        print("Deleting... %s / %s" % (index + 1, len(pipelineData)))
        arguments["filePath"] = file
        delete(**arguments)


def TASK_copy(pipelineData, arguments, iteratorConfig):
    arguments["files"] = pipelineData
    copy(**arguments)
