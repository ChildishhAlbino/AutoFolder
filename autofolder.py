import json
from utils import inFileMask
from AFEngineUtils import getConfigValues, getPipelineTaskValues, getTaskMethod, getFiles
from filters import applyFilters


def main():
    with open("./autofolder-config.json") as f:
        data = json.load(f)
    (startingFolder, globalFileMasks, pipeline) = getConfigValues(data)

    for pipelineTask in pipeline:
        print()
        (id, fileMask, task, arguments, iterator,
         filter) = getPipelineTaskValues(pipelineTask)
        files = getFiles(startingFolder)
        print("Applying file mask %s to %s files." % (fileMask, len(files)))
        maskedItems = [item for item in files if inFileMask(
            item, fileMask, globalFileMasks)]
        # apply filters
        filtered = applyFilters(filter, maskedItems)
        print("Executing pipeline task: %s on %s files" %
              (id, len(filtered)))

        task = getTaskMethod(task)
        if(task != None):
            task(filtered, arguments, iterator)


if (__name__ == "__main__"):
    main()
