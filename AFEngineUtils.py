from tasks import TASK_convert, TASK_rename, TASK_delete, TASK_unzip, TASK_copy
from os import scandir, walk
from os.path import isdir

tasks = {
    "convert": TASK_convert,
    "copy": TASK_copy,
    "delete": TASK_delete,
    "unzip": TASK_unzip
}


def getConfigValues(config):
    return (
        config["starting-folder"],
        config["globalFileMasks"],
        config["pipeline"]
    )


def getPipelineTaskValues(pipelineTask):
    return (
        pipelineTask["id"],
        pipelineTask.get("fileMask"),
        pipelineTask["task"],
        pipelineTask.get("arguments", {}),
        pipelineTask.get("iterator"),
        pipelineTask.get("filters")
    )


def getTaskMethod(task):
    return tasks.get(task)


def getFilterValues(filterConfig):
    return [(
        f["type"],
        f["fields"]
    ) for f in filterConfig]


def getFilterFieldValues(filterField):
    return (
        filterField["fieldName"],
        filterField["condition"],
        filterField["value"],
        filterField.get("valueOptions")
    )
