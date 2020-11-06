# from utils import getVideoDuration
from dataUtils import fillConditionValue
from pathlib import Path
from AFEngineUtils import getFilterValues, getFilterFieldValues
from utils import getVideoDuration, getImageResolution


def applyFilters(filters, pipelineData, globalFileMasks):
    if(filters == None):
        return pipelineData
    filters = getFilterValues(filters)
    filtered = pipelineData
    for (filterType, filterFields) in filters:
        filterFunction = filters_types.get(filterType)
        if(filterFunction):
            filtered = filterFunction(filterFields, filtered, globalFileMasks)
    return filtered


def filterVideos(filterFields, pipelineData, globalFileMasks):
    filtered = pipelineData
    for filterField in filterFields:
        (fieldName, filterCondition, conditionValue,
         valueOptions) = getFilterFieldValues(filterField)
        print(fieldName, filterCondition, conditionValue)
        fieldValue = video_filter_fields[fieldName]
        condition = conditions[filterCondition]
        print("ABOUT TO FILTER")
        filtered = [item for item in filtered if condition(
            fieldValue(item), conditionValue)]
    return filtered


def filterImages(filterFields, pipelineData, globalFileMasks):
    print("filter images")
    filtered = pipelineData
    for filterField in filterFields:
        (fieldName, filterCondition, conditionValue,
         valueOptions) = getFilterFieldValues(filterField)
        print(fieldName, filterCondition, conditionValue)
        fieldValue = image_filter_fields[fieldName]
        condition = conditions[filterCondition]
        filtered = [item for item in filtered if condition(
            fieldValue(item), conditionValue)]
    return filtered


def filterFiles(filterFields, pipelineData, globalFileMasks):
    print("filter files")
    filtered = pipelineData
    for filterField in filterFields:
        (fieldName, filterCondition, conditionValue,
         valueOptions) = getFilterFieldValues(filterField)
        filledConditionValue, filledLabel = fillConditionValue(
            conditionValue, valueOptions, {"globalFileMasks": globalFileMasks})
        fieldValue = file_filter_fields[fieldName]
        condition = conditions[filterCondition]
        filtered = [item for item in filtered if condition(
            fieldValue(item), filledConditionValue)]

        print(fieldName, filterCondition, filledLabel)
    return filtered


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
