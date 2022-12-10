user = {
    'aufa':'yepyepyep',
    'rakha':'hedon',
    'kafi':'player',
    'dafeb':'dafap',
    'dito':'meong'
}

def checkValidation(username,password):
    try:
        pw = user[username]
        if pw == password:
            return True
        else:
            return False
    except:
        return False