from subgenreDict import createSubgenreDict
import glob

subgenreDict = createSubgenreDict()

DOMAIN = input("Domain of interest (acad/news)? ")

COCA_DIR = "../coca/"
WLP_FILENAME = COCA_DIR + "coca-wlp/" + DOMAIN + "/wlp_" + DOMAIN + "_*.txt"
all_files = glob.glob(WLP_FILENAME)

subgenreCounts = {}

for filename in all_files:
    f = open(filename, encoding='windows-1252')
    prevID = None
    raw_data = f.readlines()
    for line in raw_data:
        sID = line.split('\t')[0]
        if sID != prevID:
            subgenreID = subgenreDict[sID]
            if subgenreID not in subgenreCounts:
                subgenreCounts[subgenreID] = 1
            else:
                subgenreCounts[subgenreID] += 1
            prevID = sID
    f.close()

print(subgenreCounts["151"])
