
import argparse
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def get_args():
    parser = argparse.ArgumentParser(description="RSA keygen")
    parser.add_argument("-k", "--key", help="Key file", default="pub.pem")
    parser.add_argument("-s", "--original", help="Original file", default="data/secret_file.txt")
    parser.add_argument("-o", "--output", help="Output file", default="data/output")
    parser.add_argument("-d", "--decrypt", default=False, action="store_true")
    return parser.parse_args()

def encrypt_file(public_key, message, encrypted_file):
    
    
    ciphertext = public_key.encrypt(
        message,
        padding.PKCS1v15() # not recommended for new protocols
    )
    
    with open(encrypted_file, "wb") as file:
        file.write(ciphertext)

def decrypt_file(private_key, cipher_text, decrypted_file):
    
    plaintext = private_key.decrypt(
        cipher_text,
        padding.PKCS1v15()
    )   
    
    with open(decrypted_file, "wb") as file:
        file.write(plaintext)
    
if __name__ == "__main__":
    args = get_args()
    
   
    original_file = args.original
    output_file = args.output
    decrypt = args.decrypt

    if decrypt:
        private_file = args.key
        ## Decrypt
        with open(private_file, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        
        with open(original_file, "rb") as file:
            cipher_text = file.read()
            
        
        decrypt_file(private_key, cipher_text, output_file)
    
    else:
        public_file = args.key
        ## Encrypt
        with open(public_file, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
            )
        
        with open(original_file, "rb") as file:
            message = file.read()
        
        encrypt_file(public_key, message, output_file)
        