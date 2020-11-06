# These are the actual functions that will be run by the AF Engine to transform files.
# They handle validation logic and extract boiler plate from the actual utility functions.
from utils import convert, rename, unzip, delete, copy
from iterators import getIteratorData
from dataUtils import createKwargs


def TASK_convert(pipelineData, arguments, iteratorConfig):
    print("Converting %s files!" % (len(pipelineData)))
    for file in pipelineData:
        # if iterator, generator iterator response.
        if(iteratorConfig):
            iterationData = getIteratorData(iteratorConfig, file)

            kwargsArray = [createKwargs(arguments, file, iteration)
                           for iteration in iterationData]

            print("Iterator detected! Converting file into %s files!" %
                  (len(kwargsArray)))

            for kwargs in kwargsArray:
                convert(**kwargs)
        else:
            arguments["inputPath"] = file
            convert(**arguments)


def TASK_rename(pipelineData, arguments, iteratorConfig):
    for file in pipelineData:
        rename(file, arguments["newFileName"])


def TASK_unzip(pipelineData, arguments, iteratorConfig):
    for file in pipelineData:
        arguments["archivePath"] = file
        unzip(**arguments)


def TASK_delete(pipelineData, arguments, iteratorConfig):
    for file in pipelineData:
        arguments["filePath"] = file
        delete(**arguments)


def TASK_copy(pipelineData, arguments, iteratorConfig):
    arguments["files"] = pipelineData
    copy(**arguments)
