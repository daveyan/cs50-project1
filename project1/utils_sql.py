def create_user_table(db):
    query = "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, firstname VARCHAR NOT NULL, lastname VARCHAR NOT NULL);"
    db.execute(query)
    db.commit()

def create_password_table(db):
    query = "CREATE TABLE IF NOT EXISTS password (id SERIAL PRIMARY KEY, user_id SERIAL REFERENCES users (id), password VARCHAR NOT NULL);"
    db.execute(query)
    db.commit()
