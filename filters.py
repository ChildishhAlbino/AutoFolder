# from utils import getVideoDuration
from dataUtils import fillConditionValue
from pathlib import Path
from AFEngineUtils import getFilterValues, getFilterFieldValues
from utils import getVideoDuration, getImageResolution
from uiUtils import logFiltered
from concurrent.futures import ThreadPoolExecutor

filter_data_cache = {}


def applyFilters(filledFilters, pipelineData, globalFileMasks):
    global filter_data_cache
    if(filledFilters == None):
        return pipelineData
    filledFilters = getFilterValues(filledFilters)
    totalFiltered = []
    for (filterType, filterFields) in filledFilters:
        filterTypeMapping = filter_type_fields.get(filterType)
        if(filterTypeMapping):
            filtered = applyFilterFields(
                filterTypeMapping,
                filterFields,
                pipelineData if len(totalFiltered) == 0 else totalFiltered,
                globalFileMasks)
            totalFiltered += filtered
    filter_data_cache = {}
    return list(set(totalFiltered))


def applyFilterFields(filterTypeMapping, filterFields, pipelineData, globalFileMasks):
    filtered = pipelineData
    for filterField in filterFields:

        (fieldName, filterCondition, conditionValue,
         valueOptions) = getFilterFieldValues(filterField)
        print("Filtering %s files based on %s." %
              (len(filtered), fieldName))
        filledConditionValue, filledLabel = fillConditionValue(
            conditionValue, valueOptions, {"globalFileMasks": globalFileMasks})
        fieldValue = filterTypeMapping[fieldName]
        condition = conditions[filterCondition]
        filtered = rawFilter(fieldValue, condition,
                             filledConditionValue, filtered, fieldName)
    return filtered


def rawFilter(fieldValue, condition, conditionValue, collection, fieldName):
    global filter_data_cache
    values = []
    length = len(collection)
    generated_data = filter_data_cache.get(fieldName)
    if not generated_data:
        print("Generating filter field data...")
        with ThreadPoolExecutor() as executor:
            res = executor.map(handleMtFilter(
                fieldValue, collection, length), collection)
            values = [item for item in res]
            filter_data_cache[fieldName] = values
    else:
        print("Using cached filter field data...")
        values = generated_data
    zipped = zip(
        collection, values)
    zipList = list(zipped)
    collectionSize = len(zipList)
    filtered = [filePath for filePath,
                value in zipList if logCondition(condition, value, conditionValue, collectionSize, zipList.index((filePath, value)))]
    return filtered


def logCondition(condition, value, conditionValue, collectionSize, itemIndex):
    res = condition(value, conditionValue)
    logFiltered(itemIndex, None, None, collectionSize=collectionSize)
    return res


def printItem(item, collection):
    print(f"{collection}/{len(collection)}")
    return item


def handleMtFilter(fieldValue, collection, length):
    return lambda filePath: logMTFilter(filePath, fieldValue, collection, length)


def logMTFilter(filePath, fieldValue, collection, length):
    logFiltered(collection.index(filePath), filePath, collection)
    return fieldValue(filePath)


video_filter_fields = {
    "duration": getVideoDuration,
}

image_filter_fields = {
    "resolution": getImageResolution
}

file_filter_fields = {
    "fileName": lambda f: f
}


filter_type_fields = {
    "video": video_filter_fields,
    "image": image_filter_fields,
    "file": file_filter_fields
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
