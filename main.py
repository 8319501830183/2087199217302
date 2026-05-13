import os
from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes


def get_file(filepath: str):
    if os.path.exists(filepath):
        return filepath
    else:
        raise FileNotFoundError(f"File [{filepath}] does not exist")


def encrypt_file():
    a = input("File: ")
    file = get_file(a)
    key = get_random_bytes(32)
    
    os.makedirs("./encrypted_data", exist_ok=True)
    
    with open(file, "rb") as filedata:
        raw_data = filedata.read() 
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(raw_data)
        with open("./encrypted_data/file.ed", "wb") as ofile:
            ofile.write(ciphertext)
        with open("./encrypted_data/file.dk", "wb") as ddfile:
            ddfile.write(cipher.nonce)  
            ddfile.write(tag)          
            ddfile.write(key)           
    print("OK.")


def decrypt_file():
    a = input("Data File (.ed): ")
    dfile = get_file(a)
    b = input("Decode Key File (.dk): ")
    ddfile = get_file(b)
    os.makedirs("./decode_data", exist_ok=True)
    with open(dfile, "rb") as filedata:
        ciphertext = filedata.read()
        
    with open(ddfile, "rb") as key_file:
        nonce = key_file.read(16)
        tag = key_file.read(16)
        key = key_file.read(32)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        try:
            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
            with open("./decode_data/file.decode", "wb") as ofile:
                ofile.write(decrypted_data)
            print("OK.")
        except ValueError:
            print("ERROR: Invalid key")


choose = int(input("1. encrypt file\n2. decrypt file\n"))
if choose == 1:
    encrypt_file()
elif choose == 2:
    decrypt_file()
