user = {
    'user1':'asdf',
    'dafeb':'dfa123',
    'rakhaw':'wipii123'
}

def validateUser(username,password):
    try:
        pw = user[username]
        if pw == password:
            return True
        else:
            return False
    except:
        return False