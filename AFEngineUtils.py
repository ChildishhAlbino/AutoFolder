from tasks import TASK_convert, TASK_rename, TASK_delete, TASK_unzip, TASK_copy
from os import scandir, walk
from os.path import isdir
from importlib import import_module

tasks = {
    "convert": TASK_convert,
    "copy": TASK_copy,
    "delete": TASK_delete,
    "unzip": TASK_unzip,
    "rename": TASK_rename,
}

modules = {}


def getConfigValues(config):
    return (
        config["starting-folder"],
        config["globalFileMasks"],
        config["pipeline"],
        config.get("custom", []),
        config.get("dryRun", False)
    )


def getPipelineTaskValues(pipelineTask):
    return (
        pipelineTask["id"],
        pipelineTask.get("fileMask"),
        pipelineTask["task"],
        pipelineTask.get("arguments", {}),
        pipelineTask.get("iterator"),
        pipelineTask.get("filters"),
        pipelineTask.get("shallow", False),
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


def importCustomTasks(customTasks):
    for customTask in customTasks:
        module_name = customTask["module"]
        task_function_name = customTask["taskFunction"]
        task_name = customTask["taskName"]
        if(module_name not in modules.keys()):
            modules[module_name] = importPythonModule(module_name)
        task_function = getDefinitionFromModule(
            modules[module_name], task_function_name)
        tasks[task_name] = task_function


def importPythonModule(module_name):
    try:
        module = import_module(module_name)
        return module
    except ModuleNotFoundError as e:
        print(e)
        raise Exception("Error importing python dependencies.")


def getDefinitionFromModule(module, methodName):
    if(hasattr(module, methodName)):
        try:
            func = getattr(module, methodName)
            return func
        except AttributeError as e:
            print(e)
            print("There was an attribute error.")
        except:
            print("There was some other error")
    else:
        raise Exception(
            "Couldn't find a method with that name in the module.")
