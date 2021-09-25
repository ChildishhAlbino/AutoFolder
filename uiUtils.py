

def logFiltered(index, item, collection, collectionSize: int = None):
    length = len(collection) if collectionSize is None else collectionSize
    if(length == 0):
        return item
    itemNo = index + 1
    chunkSize = int(length / 10)
    if(chunkSize == 0):
        return item
    if(index == 0):
        print("0 percent complete")
    elif(itemNo % chunkSize == 0):
        percentInt = round(itemNo / length * 100, 0)
        print("%s percent complete." % (percentInt))
    return item
