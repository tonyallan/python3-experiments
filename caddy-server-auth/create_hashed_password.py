# a quick program to create (an insecure) hashed and salted password.
# see https://docs.python.org/3/library/hashlib.html#randomized-hashing

import base64
import hashlib
import secrets


def create_password(password):
    salt = secrets.token_bytes(8)

    h = hashlib.blake2b(salt=salt)
    h.update(password.encode('utf-8'))
    hashed_password = h.digest()

    return base64.b64encode(salt + hashed_password).decode('utf-8')


def check_password(password, hashed_and_salted_password):
    password_to_check = base64.b64decode(hashed_and_salted_password.encode('utf-8'))
    salt = password_to_check[:8]
    hashed_password = password_to_check[8:]

    h = hashlib.blake2b(salt=salt)
    h.update(password.encode('utf-8'))

    return hashed_password == h.digest()


if __name__ == '__main__':
    password = input('Enter password: ')
    password_to_store = create_password(password)
    print(f'{password_to_store}')

    test = check_password(password, password_to_store)
    print('Passwords are the same', test)
