import sqlite3
import csv
import glob
from tqdm import tqdm

# Create connection to coca.db database
conn = sqlite3.connect('coca.db')
# Create cursor
c = conn.cursor()

##############################################

# Populate the lexicon table
print("\nLexicon table will now be populated...")
LEXICON = "/home/mia/phd/cancer/coca/lexicon.txt"

with open(LEXICON, 'r', encoding='windows-1252') as f:
    num_records = 0
    for row in tqdm(f):
        c.execute("INSERT INTO lexicon VALUES (?,?,?,?)", row.strip().split('\t'))
        conn.commit()
        num_records += 1

print('\n{} records transferred to lexicon table'.format(num_records))

##############################################

# Populate the sources table
print("\nSources table will now be populated...")
SOURCES = "/home/mia/phd/cancer/coca/sources.txt"

with open(SOURCES, 'r', encoding='iso-8859-1') as f:
    num_records = 0
    for row in tqdm(f):
        c.execute("INSERT INTO sources VALUES (?,?,?,?,?,?)", row.strip().split('\t'))
        conn.commit()
        num_records += 1

print('\n{} records transferred to sources table'.format(num_records))

##############################################

# Populate the subgenres table
print("\nSubgenres table will now be populated...")
SUBGENRES = "/home/mia/phd/cancer/coca/coca-subgenres.txt"

with open(SUBGENRES, 'r', encoding='us-ascii') as f:
    num_records = 0
    for row in tqdm(f):
        c.execute("INSERT INTO subgenres VALUES (?,?)", row.strip().split('\t'))
        conn.commit()
        num_records += 1

print('\n{} records transferred to subgenres table'.format(num_records))

##############################################


# Populate the coca table
print("\nCOCA table will now be populated...")
COCA = "/home/mia/phd/cancer/coca/coca-db/*/*.txt"
COCA_FILES = glob.glob(COCA)

num_records = 0
for file in tqdm(COCA_FILES):
    with open(file, 'r', 'us-ascii') as f:
        for row in f:
            c.execute("INSERT INTO coca VALUES (?,?,?)", row.strip().split('\t'))
            conn.commit()
            num_records += 1

print('\n{} records transferred to coca table'.format(num_records))

# Commit changes to database
conn.commit()
# Close connection to database
conn.close()
