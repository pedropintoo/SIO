import argparse
import getpass
from symmetric_keygen import keygen, keygen_salt, SALT_LEN
from AES128 import enc_AES128_ECB, dec_AES128_ECB, enc_AES128_CBC, dec_AES128_CBC
from AES128_utils import pad, unpad
from PIL import Image


def get_options():
    parser = argparse.ArgumentParser(description='Encrypt and Decrypt files using AES-128 ECB or CBC mode')
    parser.add_argument('mode', type=str, help='Mode of operation: ECB or CBC')
    parser.add_argument('input_file', type=str, help='Input file to encrypt/decrypt')
    parser.add_argument('output_file', type=str, help='Output file to write the result')
    parser.add_argument('--decrypt', action='store_true', help='Decrypt the input file')
    return parser.parse_args()

def enc_ECB(pwd, input_file, output_file):
    salt, key, _ = keygen(pwd)
    
    with open(input_file, 'rb') as f:
        plain_text = pad(f.read()) ## Padded

    ## Encrypt the file content
    cipher_text = salt + enc_AES128_ECB(key, plain_text)

    with open(output_file, 'wb') as f:
        f.write(cipher_text)
    
    return cipher_text

def dec_ECB(pwd, input_file, output_file):
    with open(input_file, 'rb') as f:
        cipher_text = f.read()

    ## Extract the salt and key
    salt = cipher_text[:SALT_LEN]
    key, iv = keygen_salt(pwd, salt)
    cipher_text = cipher_text[SALT_LEN:]

    ## Decrypt the file content
    plain_text = bytes.fromhex(dec_AES128_ECB(key, cipher_text))
    plain_text = unpad(plain_text)

    with open(output_file, 'wb') as f:
        f.write(plain_text)
    
    return plain_text

def enc_CBC(pwd, input_file, output_file):
    salt, key, iv = keygen(pwd)
    
    with open(input_file, 'rb') as f:
        plain_text = pad(f.read()) ## Padded

    ## Encrypt the file content
    cipher_text = salt + enc_AES128_CBC(key, iv, plain_text)

    with open(output_file, 'wb') as f:
        f.write(cipher_text)
    
    return cipher_text

def dec_CBC(pwd, input_file, output_file):
    with open(input_file, 'rb') as f:
        cipher_text = f.read()

    ## Extract the salt and key
    salt = cipher_text[:SALT_LEN]
    key, iv = keygen_salt(pwd, salt)
    cipher_text = cipher_text[SALT_LEN:]

    ## Decrypt the file content
    plain_text = bytes.fromhex(dec_AES128_CBC(key, iv, cipher_text))
    plain_text = unpad(plain_text)

    with open(output_file, 'wb') as f:
        f.write(plain_text)
    
    return plain_text

if __name__ == "__main__":
    
    
    options = get_options()
    print("====================================")
    print("Mode: " + options.mode)
    print("Input File: " + options.input_file)
    print("Output File: " + options.output_file)
    print("====================================")
    mode = options.mode
    input_file = options.input_file
    output_file = options.output_file




    pwd = bytes(getpass.getpass() , 'utf-8')
    
    ## Decryption -----------------------------------
    
    if options.decrypt:
        print("Decrypting...")
        if mode == "ECB":
            plain_text = dec_ECB(pwd, input_file, output_file)
            
        elif mode == "CBC":    
            plain_text = dec_CBC(pwd, input_file, output_file)
            
        else:
            print("ERROR. Provide valid arguments!")
            exit(1)
        
        print("====================================")
        print("Decrypted File: " + output_file)
        print("====================================")
        exit(0)
    
    ## Encryption -----------------------------------
    
    if mode == "ECB":
        cipher_text = enc_ECB(pwd, input_file, output_file)
        
    elif mode == "CBC":    
        cipher_text = enc_CBC(pwd, input_file, output_file)
        
    else:
        print("ERROR. Provide valid arguments!")
        exit(1)
    
    
    print("====================================")
    print("Encrypted File: " + output_file)
    if input_file.endswith('.bmp'):
        print("Binary as Image: (it will open in a new window)")
        
        ## Original Image
        img = Image.open(input_file)
        img_data = img.tobytes()
        width, height = img.size
        
        ## Encrypted Image
        enc_img = Image.frombytes(img.mode, (width, height), cipher_text[:len(img_data)])
        # bmp mode is upside down
        enc_img = enc_img.transpose(Image.FLIP_TOP_BOTTOM)
        enc_img = enc_img.transpose(Image.FLIP_LEFT_RIGHT)
        
        ## Show comparison
        combined_img = Image.new("RGB", (width*2, height))
        combined_img.paste(img, (0, 0))
        combined_img.paste(enc_img, (width, 0))
        combined_img.show()
    print("====================================")
    
        