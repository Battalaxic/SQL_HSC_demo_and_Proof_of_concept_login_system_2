import bcrypt

'''Salt and hash are of string data type, converted from byte data type'''

def encrypt_password(plain_text):
    plain_text_in_bytes = plain_text.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(plain_text_in_bytes, salt)
    hash = hash.decode("utf-8")
    return hash

def check_password(entered_passwd, hash_to_compare_to):
    entered_passwd_in_bytes = entered_passwd.encode('utf-8')
    hash_to_compare_to = hash_to_compare_to.encode('utf-8')
    is_true_password = bcrypt.checkpw(entered_passwd_in_bytes, hash_to_compare_to)
    return is_true_password

if __name__ == '__main__':
    hash_to_compare_to = encrypt_password("password1")
    print(check_password("password1", hash_to_compare_to))