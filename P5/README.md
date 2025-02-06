# Gen key RSA
```bash
python rsa_keygen.py --public ./pub.pem --private ./priv.pem --length 4096
```

### Encrypt
```bash
python rsa_files.py --key pub.pem --origin data/secret_file.txt --output data/secret_file_encrypted
```

### Decrypt
```bash
python rsa_files.py --key priv.pem --origin data/secret_file_encrypted --output data/secret_file_decrypted.txt --decrypt
```

# Using SSH
```bash
ssh-keygen -t rsa
```

