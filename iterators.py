from utils import getVideoDuration


def ITERATOR_FIELD_videoDuration(iteratorConfig, filePath):
    iterationData = []
    duration = getVideoDuration(filePath)

    sectionDuration = iteratorConfig["value"]
    roundingThreshold = iteratorConfig["options"]["roundingThreshold"]
    rawSegments = duration / sectionDuration if sectionDuration > 0 else 1
    roundSegments = round(rawSegments)
    delta = duration - (roundSegments * sectionDuration)
    numSections = roundSegments + 1 if (
        delta > roundingThreshold) else roundSegments

    numSections = 1 if (roundSegments < 1) else numSections
    numSections = 1 if (duration < sectionDuration) else numSections
    for iteration in range(0, numSections):
        iterationData.append((sectionDuration, iteration*sectionDuration))
    return iterationData


def ITERATOR_forEvery(iteratorData):
    return iteratorData


def getIteratorData(iteratorConfig, filePath):
    fieldName = iteratorConfig["fieldName"]
    rawIterationData = iteration_fields[fieldName](iteratorConfig, filePath)
    iteratorFunction = iteratorConfig["function"]
    finalIterationData = iterators[iteratorFunction](rawIterationData)
    return finalIterationData


iteration_fields = {
    "videoDuration": ITERATOR_FIELD_videoDuration
}

iterators = {
    "forEvery": ITERATOR_forEvery
}
