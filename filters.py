# from utils import getVideoDuration
from dataUtils import fillConditionValue
from pathlib import Path
from AFEngineUtils import getFilterValues, getFilterFieldValues
from utils import getVideoDuration, getImageResolution
from uiUtils import logFiltered
from concurrent.futures import ThreadPoolExecutor


def applyFilters(filledFilters, pipelineData, globalFileMasks):
    if(filledFilters == None):
        return pipelineData
    filledFilters = getFilterValues(filledFilters)
    filtered = pipelineData
    for (filterType, filterFields) in filledFilters:
        filterFunction = filters_types.get(filterType)
        if(filterFunction):
            filtered = filterFunction(filterFields, filtered, globalFileMasks)
    return filtered


def filterVideos(filterFields, pipelineData, globalFileMasks):
    filtered = pipelineData
    for filterField in filterFields:
        (fieldName, filterCondition, conditionValue,
         valueOptions) = getFilterFieldValues(filterField)
        fieldValue = video_filter_fields[fieldName]
        condition = conditions[filterCondition]
        filtered = rawFilter(fieldValue, condition,
                             conditionValue, filtered)
    return filtered


def filterImages(filterFields, pipelineData, globalFileMasks):
    filtered = pipelineData
    for filterField in filterFields:
        (fieldName, filterCondition, conditionValue,
         valueOptions) = getFilterFieldValues(filterField)
        fieldValue = image_filter_fields[fieldName]
        condition = conditions[filterCondition]
        filtered = rawFilter(fieldValue, condition,
                             conditionValue, filtered)
    return filtered


def filterFiles(filterFields, pipelineData, globalFileMasks):
    filtered = pipelineData
    for filterField in filterFields:
        (fieldName, filterCondition, conditionValue,
         valueOptions) = getFilterFieldValues(filterField)
        filledConditionValue, filledLabel = fillConditionValue(
            conditionValue, valueOptions, {"globalFileMasks": globalFileMasks})
        fieldValue = file_filter_fields[fieldName]
        condition = conditions[filterCondition]
        filtered = rawFilter(fieldValue, condition,
                             filledConditionValue, filtered)
    return filtered


def rawFilter(fieldValue, condition, conditionValue, collection):
    values = []
    length = len(collection)
    with ThreadPoolExecutor() as executor:
        values = executor.map(handleMtFilter(
            fieldValue, collection, length), collection)
    filtered = [filePath for filePath, value in zip(
        collection, values) if condition(value, conditionValue)]
    # filtered = [item for index, item in enumerate(collection) if condition(
    #     logFiltered(index, fieldValue(item), collection), conditionValue)]
    return filtered


def handleMtFilter(fieldValue, collection, length):
    return lambda filePath: logMTFilter(filePath, fieldValue, collection, length)


def logMTFilter(filePath, fieldValue, collection, length):
    logFiltered(collection.index(filePath), filePath, collection)
    return fieldValue(filePath)


filters_types = {
    "video": filterVideos,
    "image": filterImages,
    "file": filterFiles


}

video_filter_fields = {
    "duration": getVideoDuration,
}

image_filter_fields = {
    "resolution": getImageResolution
}

file_filter_fields = {
    "fileName": lambda f: f
}

conditions = {
    "==": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    "<=": lambda x, y: x <= y,
    "<": lambda x, y: x < y,
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y,
    "in": lambda x, y: x in y,
    "any-item-in": lambda x, y: len([i for i in y if Path(i).stem in x]) > 0
}
