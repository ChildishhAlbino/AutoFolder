import json
from utils import inFileMask, printSeparator
from AFEngineUtils import getConfigValues, getPipelineTaskValues, getTaskMethod, importCustomTasks
from filters import applyFilters
from fileUtils import getFiles
from click import clear
import uuid


def main(configLocation):
    with open(configLocation) as f:
        data = json.load(f)
    (startingFolder, globalFileMasks, pipeline,
     custom, dryRun) = getConfigValues(data)
    if(len(custom) > 0):
        importCustomTasks(custom)
    input("Press enter to run %s pipeline tasks or CTRL+C to exit. " %
          (len(pipeline)))
    instance_rand = str(uuid.uuid4())
    for index, pipelineTask in enumerate(pipeline):
        (id, fileMask, task, arguments, iterator,
         filter, shallow) = getPipelineTaskValues(pipelineTask)
        arguments["instanceRand"] = instance_rand
        print("#%s: %s\n" % (index + 1, id))
        files = getFiles(startingFolder, shallow)
        print("Applying file mask %s to %s files." % (fileMask, len(files)))
        maskedItems = [item for item in files if inFileMask(
            item, fileMask, globalFileMasks)]
        # apply filters
        print("Applying filters to %s files." % (len(maskedItems)))
        filtered = applyFilters(filter, maskedItems, globalFileMasks)
        print("Executing pipeline task: %s on %s files\n" %
              (id, len(filtered)))
        task = getTaskMethod(task)
        if task is not None and not dryRun:
            task(filtered, arguments, iterator)
        printSeparator()
    input("FINISHED! Press any key to exit.")


if __name__ == "__main__":
    clear()
    main("./autofolder-config.json")
