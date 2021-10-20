import sqlite3

# Create connection to coca.db database
conn = sqlite3.connect('coca.db')
# Create cursor
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS lexicon (
        wordID INTEGER,
        word   TEXT,
        lemma  TEXT,
        pos    TEXT
    )
""")

c.execute("""
CREATE TABLE IF NOT EXISTS sources (
        textID      INTEGER,
        year        INTEGER,
        genre       TEXT,
        subgenreID  INTEGER,
        sourceTitle TEXT,
        textTitle   TEXT
    )
""")

c.execute("""
CREATE TABLE IF NOT EXISTS coca (
        textID INTEGER,
        ID     INTEGER,
        wordID INTEGER
    )
""")

c.execute("""
CREATE TABLE IF NOT EXISTS subgenres (
        subgenreID INTEGER,
        subgenre   TEXT
    )
""")

# Commit changes to database
conn.commit()
# Close connection to database
conn.close()
