def createSubgenreDict():
    FILENAME = "../../coca/sources.txt"

    subgenreDict = {}
    with open(FILENAME, encoding='iso-8859-1') as f:
        for line in f:
            line = line.rstrip().split("\t")
            if line[0] not in subgenreDict:
                subgenreDict[line[0]] = line[3]

    return subgenreDict
