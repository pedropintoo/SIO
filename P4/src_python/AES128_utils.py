from cryptography.hazmat.primitives import padding
from AES128 import *

BLOCK_SIZE = 128

def pad(plain_text):
    padder = padding.PKCS7(BLOCK_SIZE).padder()

    padded_data = padder.update(plain_text)
    padded_data += padder.finalize()

    return padded_data

def unpad(padded_data):
    unpadder = padding.PKCS7(BLOCK_SIZE).unpadder()

    data = unpadder.update(padded_data)
    data += unpadder.finalize()
    
    return data
    

TEST_SAMPLES = {
    "AES-128-TEST": {
        "KEY"         : "edfdb257cb37cdf182c5455b0c0efebb",
        "PLAINTEXT"   : "00",
        "CIPHERTEXT"  : "1c8cf23a5999dc4b8ae7b52f8c471225"
    },
    "AES-128-ECB-TEST": {
        "KEY"         : "7723d87d773a8bbfe1ae5b081235b566",
        "PLAINTEXT"   : "1b0a69b7bc534c16cecffae02cc5323190ceb413f1db3e9f0f79ba654c54b601",
        "CIPHERTEXT"  : "ad5b089515e7821087c61652dc477ab13ee2e6dCBC921409cd7060ea9d2945792cb90e7912c7c42662a651db32a313a5"
    },
    "AES-128-CBC-TEST": {
        "KEY"         : "0700d603a1c514e46b6191ba430a3a0c",
        "IV"          : "aad1583cd91365e3bb2f0c3430d065bb",
        "PLAINTEXT"   : "068b25c7bfb1f8bdd4cfc908f69dffc5ddc726a197f0e5f7",
        "CIPHERTEXT"  : "c4dc61d9725967a3020104a9738f2386b2a3deac1540e33e42c5a19e60152ce4"
    }
}

if __name__ == "__main__":
    
    tests = ["AES-128-TEST", "AES-128-ECB-TEST", "AES-128-CBC-TEST"]

    for mode in tests:

        key = bytes.fromhex(TEST_SAMPLES[mode]["KEY"])
        ## padding
        plain_text = pad(bytes.fromhex(TEST_SAMPLES[mode]["PLAINTEXT"]))
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

        ## unpading
        decrypted_text = unpad(bytes.fromhex(decrypted_text)).hex()
        plain_text_validation = TEST_SAMPLES[mode]["PLAINTEXT"]

        print("Plain Text: " + plain_text_validation)
        print("Cipher Text: " + cipher_text.hex())
        print("Decrypted Text: " + decrypted_text)
        
        
        assert(decrypted_text == plain_text_validation)
        assert (cipher_text == cipher_validation)
        print("Success: " + mode)
        print("============================")
        


