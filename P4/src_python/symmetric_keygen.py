import getpass
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_LEN = 16

def keygen(pwd):
    # Salts should be randomly generated
    salt = os.urandom(16)
    key, iv = keygen_salt(pwd, salt)
    return salt, key, iv

## Key Derivation Function
def keygen_salt(pwd, salt):
    # derive
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), # output is 256 bits -> 32 bytes
        length=32,
        salt=salt,
        iterations=480000,
    )

    full_key = kdf.derive(pwd)

    key = full_key[:16]
    iv = full_key[16:]
    return key, iv # sliced


if __name__ == "__main__":
    pwd = bytes(getpass.getpass() , 'utf-8')
    salt, key, iv = keygen(pwd)

    print("Salt:", salt)
    print("Key:", key)
    print("IV:", iv)

    assert(is_correct_password(salt, key, iv))