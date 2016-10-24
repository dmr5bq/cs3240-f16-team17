from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES
import os
import struct

def secret_string(st, pk):
    encrypted = pk.encrypt(st.encode(), 32)
    return encrypted

def encrypt_file(f, sk):
    initVector = os.urandom(16)
    AES_enc = AES.new(sk, AES.MODE_CBC, initVector)
    filesize = os.path.getsize(f)
    try:
        with open(f, 'rb') as file:
            with open(f + '.enc', 'wb') as outFile:
                outFile.write(struct.pack('<Q', filesize))
                outFile.write(initVector)
                while True:
                    chunk = file.read(1024)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += (' ' * (16 - len(chunk) % 16)).encode()
                    outFile.write(AES_enc.encrypt(chunk))
                outFile.close()
            file.close()
        return True
    except FileNotFoundError:
        print("File: " + f + " not found!")
        return False

def decrypt_file(f, sk):
    if '.enc' == f[len(f)-4:len(f)]:
        try:
            with open(f, 'rb') as file:
                fSize = struct.unpack('<Q', file.read(struct.calcsize('Q')))[0]
                initVector = file.read(16)
                AES_dec = AES.new(sk, AES.MODE_CBC, initVector)
                with open('DEC_' + f[0:len(f)-4], 'wb') as outFile:
                    while True:
                        chunk = file.read(1024)
                        if len(chunk) == 0:
                            break
                        outFile.write(AES_dec.decrypt(chunk))
                    outFile.truncate(fSize)
                    outFile.close()
                file.close()
            return True
        except FileNotFoundError:
            print("File: ", f, " not found!")
            return False
    else:
        print("Invalid extension, must end in .enc")
        return False
    
if __name__ == "__main__":
    rand = Random.new().read
    key = RSA.generate(1024, rand)

    public_key = key.publickey()
    print((key.decrypt(secret_string("Hello world", public_key))).decode())

    sym_key = "SuperISecretIKey"

    encrypt_file("test.jpg",sym_key)
    decrypt_file("test.jpg.enc", sym_key)
