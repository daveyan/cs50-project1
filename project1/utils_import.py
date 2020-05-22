import sys

def create_db(db):
    query = "CREATE TABLE IF NOT EXISTS books (id SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year INT NOT NULL);"
    db.execute(query)
    db.commit()

def batch_insert_db(db,total ,list):
    i = 0
    for isbn, title, author, year in list:
        insert_db(db,isbn, title, author, year)
        #Added progress bar since the inserts take quite a bit of time
        progress_bar(i, total)
        i+= 1
    db.commit()


def insert_db(db, i, t, a, y):
    db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year);",{"isbn":i, "title":t, "author": a, "year": y})

def check_db(db, total):
    try:
        count = db.execute("SELECT COUNT(*) from books").scalar()
        if count == total:
            print(f"\nA total of {total} entries was found")
        else:
            raise Exception("Not all entries were found")
    except Exception as e:
        print(str(e))

def drop_db(db):
    query = "DROP TABLE IF EXISTS books"
    db.execute(query)
    db.commit()

def progress_bar(count, total):
    length = 100
    filled = int(round(length * count / total))
    percent = int(round((count / total) * 100))
    bar = '=' * filled + '-' * (length - filled)
    sys.stdout.write('\rImporting: [%s] %s%%\r' % (bar, percent))
    sys.stdout.flush()
