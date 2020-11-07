import json
from utils import inFileMask, printSeparator
from AFEngineUtils import getConfigValues, getPipelineTaskValues, getTaskMethod
from filters import applyFilters
from fileUtils import getFiles
from click import clear


def main(configLocation):
    with open(configLocation) as f:
        data = json.load(f)
    (startingFolder, globalFileMasks, pipeline) = getConfigValues(data)

    for index, pipelineTask in enumerate(pipeline):
        (id, fileMask, task, arguments, iterator,
         filter) = getPipelineTaskValues(pipelineTask)
        print("#%s: %s\n" % (index + 1, id))
        files = getFiles(startingFolder)
        print("Applying file mask %s to %s files." % (fileMask, len(files)))
        maskedItems = [item for item in files if inFileMask(
            item, fileMask, globalFileMasks)]
        # apply filters
        print("Applying filters to %s files." % (len(maskedItems)))
        filtered = applyFilters(filter, maskedItems, globalFileMasks)
        print("Executing pipeline task: %s on %s files" %
              (id, len(filtered)))
        task = getTaskMethod(task)
        if(task != None):
            task(filtered, arguments, iterator)
        printSeparator()
    print("FINISHED")


if (__name__ == "__main__"):
    clear()
    main("./autofolder-config.json")
