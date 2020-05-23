def insert_password(db, userid, password):
    db.execute("INSERT INTO password (user_id, password) VALUES (:userid, :password)",{"userid": userid, "password": password})
    db.commit()


def get_password(db, userid):
    result = db.execute("SELECT * FROM password WHERE user_id = :userid",{"userid": userid})
    return result.first()
