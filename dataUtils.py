
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
