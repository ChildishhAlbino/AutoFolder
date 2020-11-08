

def logFiltered(index, item, collection):
    length = len(collection)
    itemNo = index + 1
    chunkSize = int(length / 10)

    if(itemNo % chunkSize == 0):
        percentInt = round(itemNo / length * 100, 0)
        print("%s percent complete." % (percentInt))
    return item
