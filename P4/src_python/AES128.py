import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

## AES-128 (iv with zeros)
def enc_AES128(key, plain_text):
    iv = bytes.fromhex("00"*16) ## Not secure!
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(plain_text) + encryptor.finalize()
    return cipher_text

def dec_AES128(key, cipher_text):
    iv = bytes.fromhex("00"*16) ## Not secure!
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plain_text = decryptor.update(cipher_text) + decryptor.finalize()
    return plain_text.hex() ## in hex


## AES-128 ECB Mode
def enc_AES128_ECB(key, plain_text):
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(plain_text) + encryptor.finalize()
    return cipher_text

def dec_AES128_ECB(key, cipher_text):
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    plain_text = decryptor.update(cipher_text) + decryptor.finalize()
    return plain_text.hex() ## in hex


## AES-128 CBC Mode
def enc_AES128_CBC(key, iv, plain_text):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(plain_text) + encryptor.finalize()
    return cipher_text

def dec_AES128_CBC(key, iv, cipher_text):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plain_text = decryptor.update(cipher_text) + decryptor.finalize()
    return plain_text.hex() ## in hex


TEST_SAMPLES = {
    "AES-128-TEST": {
        "KEY"         : "edfdb257cb37cdf182c5455b0c0efebb",
        "PLAINTEXT"   : "1695fe475421cace3557daca01f445ff",
        "CIPHERTEXT"  : "7888beae6e7a426332a7eaa2f808e637"
    },
    "AES-128-ECB-TEST": {
        "KEY"         : "7723d87d773a8bbfe1ae5b081235b566",
        "PLAINTEXT"   : "1b0a69b7bc534c16cecffae02cc5323190ceb413f1db3e9f0f79ba654c54b60e",
        "CIPHERTEXT"  : "ad5b089515e7821087c61652dc477ab1f2cc6331a70dfc59c9ffb0c723c682f6"
    },
    "AES-128-CBC-TEST": {
        "KEY"         : "0700d603a1c514e46b6191ba430a3a0c",
        "IV"          : "aad1583cd91365e3bb2f0c3430d065bb",
        "PLAINTEXT"   : "068b25c7bfb1f8bdd4cfc908f69dffc5ddc726a197f0e5f720f730393279be91",
        "CIPHERTEXT"  : "c4dc61d9725967a3020104a9738f23868527ce839aab1752fd8bdb95a82c4d00"
    }
}

if __name__ == "__main__":
    
    tests = ["AES-128-TEST", "AES-128-ECB-TEST", "AES-128-CBC-TEST"]

    for mode in tests:

        key = bytes.fromhex(TEST_SAMPLES[mode]["KEY"])
        plain_text = bytes.fromhex(TEST_SAMPLES[mode]["PLAINTEXT"])
        cipher_validation = bytes.fromhex(TEST_SAMPLES[mode]["CIPHERTEXT"])


        if mode == "AES-128-TEST":
            ## AES-128 (iv with zeros)
            cipher_text = enc_AES128(key, plain_text) 
            decrypted_text = dec_AES128(key, cipher_text)
            
        elif mode == "AES-128-ECB-TEST":
            ## AES-128 ECB Mode
            cipher_text = enc_AES128_ECB(key, plain_text) 
            decrypted_text = dec_AES128_ECB(key, cipher_text)
        else:
            ## AES-128 CBC Mode
            iv = bytes.fromhex(TEST_SAMPLES[mode]["IV"])
            cipher_text = enc_AES128_CBC(key, iv, plain_text)
            decrypted_text = dec_AES128_CBC(key, iv, cipher_text) 

        print("Plain Text: " + plain_text.hex())
        print("Cipher Text: " + cipher_text.hex())
        print("Decrypted Text: " + decrypted_text)

        assert(decrypted_text == plain_text.hex())
        assert (cipher_text == cipher_validation)
        print("Success: " + mode)
        print("============================")


