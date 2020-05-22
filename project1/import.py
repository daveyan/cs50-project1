import csv
import os

from utils_import import drop_db
from utils_import import create_db
from utils_import import batch_insert_db
from utils_import import check_db

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main ():
    try:
    
        drop_db(db)
        create_db(db)
 
        f = open("books.csv")
        reader = csv.reader(f)

        #First line of the CSV is the header
        next(reader, None)

        row_count = 5000

        batch_insert_db(db, row_count,reader)

        check_db(db, row_count)  
    except Exception as e:
        print("Error: " + str(e))      

if __name__ == "__main__":
    main()
