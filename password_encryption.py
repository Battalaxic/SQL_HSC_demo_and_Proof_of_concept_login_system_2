import bcrypt

def encrypt_password(plain_text):
    bytes = plain_text.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return [salt, hash]

def check_password(entered_passwd, hash_to_compare_to, salt):
    bytes = entered_passwd.encode('utf-8')
    hash_to_question = bcrypt.hashpw(bytes, salt)
    if hash_to_question == hash_to_compare_to:
        return True
    else:
        return False

if __name__ == '__main__':
    print(encrypt_password("password1"))
    print(encrypt_password("password1"))
    print(encrypt_password(""))