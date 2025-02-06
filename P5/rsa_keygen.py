
import argparse
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

PUBLIC_KEY = 65537

def get_args():
    parser = argparse.ArgumentParser(description="RSA keygen")
    parser.add_argument("-p", "--public", help="Output Public key file", default="pub.pem")
    parser.add_argument("-s", "--private", help="Output Private key file", default="priv.pem")
    parser.add_argument("-l", "--length", type=int, help="Key length", default=2048)
    return parser.parse_args()


def gen(length: int):
    return rsa.generate_private_key(
        public_exponent=PUBLIC_KEY,
        key_size=length,
    )

if __name__ == "__main__":
    args = get_args()
    
    public_file = args.public
    private_file = args.private
    length = args.length
    
    print(f"Generating RSA key pair with length {length}")
    
    priv_key = gen(length)
    pub_key = priv_key.public_key()
    
    with open(public_file, "wb") as f:
        f.write(pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    with open(private_file, "wb") as f:
        f.write(priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
        

    