def create_password_table(db):
    query = "CREATE TABLE IF NOT EXISTS password (id SERIAL PRIMARY KEY, user_id SERIAL REFERENCES users (id), password VARCHAR NOT NULL);"
    db.execute(query)
    db.commit()

def insert_password(db, userid, password):
    db.execute("INSERT INTO password (user_id, password) VALUES (:userid, :password)",{"userid": userid, "password": password})
    db.commit()


def get_password(db, userid):
    result = db.execute("SELECT * FROM password WHERE user_id = :userid",{"userid": userid})
    return result.first()

def password_compare(str1, str2):
    if str1 == str2:
        return True
    else:
        return False
