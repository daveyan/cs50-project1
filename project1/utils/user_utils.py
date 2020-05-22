def password_compare(str1, str2):
    if str1 == str2:
        return True
    else:
        return False

def find_by_username(db, name):
    result = db.execute("SELECT * FROM users WHERE username = :name",{"name": name})
    return result.first()

def unique_user(db,name):
    user = find_by_username(db, name)
    if user is not None:
        return False
    else:
        return True