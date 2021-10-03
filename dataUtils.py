
from utils import inFileMask
from fileUtils import getFiles


def fillWithIterationData(iterationData, argument):
    if(argument == None):
        return argument
    (value, iterationValue) = iterationData
    if("|value|" in str(argument)):
        argument = argument.replace("|value|", str(value))
    if("|iterationValue|" in argument):
        argument = argument.replace(
            "|iterationValue|", str(iterationValue))
    return argument


def fillArguments(iterationData, arguments):
    newArguments = {}
    for parameter, argument in arguments.items():
        newArguments[parameter] = fillWithIterationData(
            iterationData, argument)
    return newArguments


def createKwargs(arguments, file, iteration):
    iterationArguments = fillArguments(iteration, arguments)
    iterationArguments["inputPath"] = file
    return iterationArguments


def fillConditionValue(rawFilterValue, valueOptions, globalData):
    filled = rawFilterValue
    if(filled == "|directoryData|"):
        filled = getFiles(valueOptions["directoryData"])
        filled = [f for f in filled if inFileMask(
            f, valueOptions["fileMask"], globalData["globalFileMasks"])]
        return (filled, "directoryData(%s)" % (valueOptions["fileMask"]))
    else:
        return (rawFilterValue, rawFilterValue)
