from base64 import encodebytes, b64encode
import uuid
from utils import renameFile
from concurrent.futures import ThreadPoolExecutor
from tasks import HANDLE_MT
from json import dump
from tasks import TASK_delete

conflicts = []


def TASK_rename_b64(pipelineData, arguments, iteratorConfig):
    ignore_conflicts = arguments.get('ignoreConflicts', False)
    print('RENAME B64')
    length = len(pipelineData)
    with ThreadPoolExecutor() as executor:
        results = executor.map(HANDLE_MT(
            arguments, iteratorConfig, getFileUUID, pipelineData, length, "Renaming Item #%s of %s"), pipelineData)
        listRes = [item for item in results]
    print(conflicts)
    if(ignore_conflicts):
        with open("./conflicts.json", 'w') as f:
            dump(conflicts, f, indent=2)
    else:
        duplicate_files = [conflict["filePath"] for conflict in conflicts]
        print(f"Deleting {len(duplicate_files)} duplicate files.")
        with open("./deleted-duplicates.json", 'w') as f:
            dump(duplicate_files, f, indent=2)
        TASK_delete(duplicate_files, {}, None)


def getFileUUID(filePath, arguments, iteratorConfig):
    print(filePath)
    finalUUID = None
    try:
        with open(filePath, 'rb') as f:
            data = f.read()
            b64Data = str(b64encode(data))
            finalB64 = b64Data[2:-1]
        rawUuid = uuid.uuid5(uuid.NAMESPACE_URL, finalB64)
        finalUUID = str(rawUuid)
        renameFile(filePath, finalUUID)
    except MemoryError as memErr:
        print(memErr)
        print("Memory Error occurred for file %s" % filePath)
    except Exception as e:
        print(e)
        conflicts.append(
            {"conflictedFileName": finalUUID, "filePath": filePath})
