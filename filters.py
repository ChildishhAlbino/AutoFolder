# from utils import getVideoDuration
from AFEngineUtils import getFilterValues, getFilterFieldValues
from utils import getVideoDuration, getImageResolution


def applyFilters(filters, pipelineData):
    if(filters == None):
        return pipelineData
    filters = getFilterValues(filters)
    filtered = pipelineData
    for (filterType, filterFields) in filters:
        filterFunction = filters_types.get(filterType)
        if(filterFunction):
            filtered = filterFunction(filterFields, filtered)
    return filtered


def filterVideos(filterFields, pipelineData):
    filtered = pipelineData
    for filterField in filterFields:
        (fieldName, filterCondition, conditionValue) = getFilterFieldValues(filterField)
        fieldValue = video_filter_fields[fieldName]
        condition = conditions[filterCondition]
        filtered = [item for item in filtered if condition(
            fieldValue(item), conditionValue)]
    return filtered


def filterImages(filterFields, pipelineData):
    print("filter images")
    filtered = pipelineData
    for filterField in filterFields:
        (fieldName, filterCondition, conditionValue) = getFilterFieldValues(filterField)
        print(fieldName, filterCondition, conditionValue)
        fieldValue = image_filter_fields[fieldName]
        condition = conditions[filterCondition]
        filtered = [item for item in filtered if condition(
            fieldValue(item), conditionValue)]
    return filtered


filters_types = {
    "video": filterVideos,
    "image": filterImages
}

video_filter_fields = {
    "duration": getVideoDuration,
}

image_filter_fields = {
    "resolution": getImageResolution
}

conditions = {
    "==": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    "<=": lambda x, y: x <= y,
    "<": lambda x, y: x < y,
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y,
    "in": lambda x, y: x in y
}
