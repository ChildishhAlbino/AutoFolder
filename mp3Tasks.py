import eyed3
from pathlib import Path
from os.path import splitext


def TASK_update_title(pipelineData, arguments, iteratorConfig):
    separator = arguments.get('separator', " - ")
    print("Updating meta")
    for filePath in pipelineData:
        print(filePath)
        fileName = Path(filePath).stem
        meta = eyed3.load(filePath)
        title = meta.tag.title
        if(title is None):
            print(fileName)
            separator_index = fileName.index(separator) if(
                separator in fileName) else len(fileName)
            meta.tag.title = fileName[:separator_index]
            meta.tag.save()
        else:
            print(title)
