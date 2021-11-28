from Corpus import Corpus
from Preprocessing import preprocessing
from helper import *
from subgenreDict import createSubgenreDict
import glob
from tqdm import tqdm
import sys, getopt

#######################################################

# relative path to the directory where all the coca files are
COCA_DIR = "../../coca/"
# relative path to output dir
OUTPUT_DIR = "../output/"

subgenreDict = createSubgenreDict()
# these values come from coca-subgenres.txt
newsIDs = [i for i in range(135, 143)]
acadIDs = [i for i in range(144, 153)]
medIDs = [150, 151]

def main(argv):
    domain = ''
    complement = False
    normalize = False
    subgenreIDs = []

    try:
        opts, args = getopt.getopt(argv,"hd:cn",["domain=",
                                                 "complement=",
                                                 "normalize="])
    except getopt.GetoptError:
        print('co-occurrence.py -d <domain> -c -n')
        sys.exit(2)

    # parse command line arguments
    for opt, arg in opts:
        if opt == '-h':
            print("co-occurrence.py -d <domain> -c -n")
            sys.exit()
        elif opt in ("-d", "--domain"):
            domain = arg
        elif opt in ("-c", "--complement"):
            # complement option is only valid for the acad domain
            if domain == 'acad':
                complement = True
        elif opt in ("-n", "--normalize"):
            normalize = True

    # set the correct target subgenre IDs
    if domain == 'acad':
        if complement:
            subgenreIDs = [i for i in acadIDs if i not in medIDs]
        else:
            subgenreIDs = [i for i in acadIDs if i in medIDs]
    elif domain == 'news':
        subgenreIDs = newsIDs
    else:
        print("\nInvalid domain\n Valid domains are 'acad' and 'news'")
        sys.exit()

    # use glob to find all the relevant files to be processed
    filename_template = COCA_DIR + "coca-wlp/" + domain + "/wlp_" + domain + "_*.txt"
    print("\nSearching for files using the template\n\t\t{}".format(filename_template))
    try:
        all_files = glob.glob(filename_template)
    except:
        print("\nCould not find appropriate files.")
        sys.exit()

    ###################################################

    # Initialize statistics variables
    cooccurrence     = {}
    cancer_count     = 0
    sent_lens        = []
    cancer_sent_lens = []

    for filename in tqdm(all_files):
        print("\nProcessing " + filename + "...")

        # Create a new corpus
        corpus = Corpus()

        # Process the data in this file
        preprocessing(filename, corpus, subgenreDict, subgenreIDs)
        corpus.diagnose()

        # Update cooccurrence dictionary with new counts
        cooccurrence = sum_update(cooccurrence, corpus.cooccurrence)

        # Update statistics
        cancer_count     += corpus.getCancerCount()
        sent_lens        += corpus.getSentLens()
        cancer_sent_lens += corpus.getCancerSentLens()

    ###################################################

    # Set the filename for the output statistics about the corpus:
    # ../output/acad_medical_statistics.txt
    # ../output/acad_non-medical_statistics.txt
    # ../output/news_statistics.txt
    specialization = ""
    if complement:
        specialization = "_non-medical"
    else:
        if domain == "acad": specialization = "_medical"

    statistics_output = OUTPUT_DIR + domain + specialization + "_statistics.txt"

    # Populate the statistics to be written to file
    statistics = []
    statistics.append("The corpus has a total of {} sentences".format(len(sent_lens)))
    statistics.append("The total number of words in the corpus is {}".format(sum(sent_lens)))
    statistics.append("The average length is {}".format(sum(sent_lens) / len(sent_lens)))
    statistics.append("There are {} sentences with 'cancer' in it".format(cancer_count))
    statistics.append("The average length of 'cancer' sentences is {}".format(sum(cancer_sent_lens) / len(cancer_sent_lens)))

    # Write statistics to file
    with open(statistics_output, "w+") as f:
        f.write('\n'.join(statistics) + '\n')

    ###################################################

    import operator

    # Set the filename for the output co-occurrence counts:
    # ../output/acad_medical_raw_counts.csv
    # ../output/acad_medical_norm_counts.csv
    # ../output/acad_non-medical_raw_counts.csv
    # ../output/acad_non-medical_norm_counts.csv
    # ../output/news_raw_counts.csv
    # ../output/news_norm_counts.csv
    count_type = "_norm" if normalize else "_raw"
    output_filename = OUTPUT_DIR + domain + specialization + count_type + "_counts.csv"

    # sort items in the dicts, optionally normalize
    if normalize:
        cooccurrencenorm = {k:(float(v)/sum(cancer_sent_lens)) for (k,v) in cooccurrence.items()}
        output_sorted = dict(sorted(cooccurrencenorm.items(), key=operator.itemgetter(1), reverse=True))
    else:
        output_sorted = dict(sorted(cooccurrence.items(), key=operator.itemgetter(1), reverse=True))

    import csv

    # write co-occurrence counts to file
    w = csv.writer(open(output_filename, "w"))
    for key, val in output_sorted.items():
        w.writerow([key, val])


##############################################################

if __name__ == "__main__":
    main(sys.argv[1:])
