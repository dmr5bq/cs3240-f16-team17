from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES3

IV = Random.get_random_bytes(8)

def _gen_key_pair():
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    return key


def secret_string(str, key):
    public_key = key.publickey()
    return public_key.encrypt(str, 32)


def encrypt_file(file, key):

    # edge cases; key is empty, key is numeric
    if key is "":
        print("Enter a valid key, encryption failed.")
        return False

    key = str(key)

    # ensure key is of correct length, pad if not
    if len(key) % 16 != 0:
        key += ' ' * (16 - len(key) % 16)

    # standard block size
    block_size = 8

    # set up the encryption module
    encryptor = DES3.new(key, DES3.MODE_CFB, IV)

    input_filename = file
    output_filename = file + '.enc'

    # read from <file>, write encrypted bytes to output <file>.enc
    with open(input_filename, 'rb') as f_input:
        with open(output_filename, 'wb') as f_output:
            while True:
                block = f_input.read(block_size)

                if len(block) == 0:
                    break
                elif len(block) % 16 == 0:
                    block += ' ' * (16 - len(block) % 16)

                cipher_block = encryptor.encrypt(block)
                f_output.write(cipher_block)
            return True

    # failure case
    return False



def decrypt_file(file, key):
    if key is "":
        print("Enter a valid key, decryption failed.")
        return False

    iv = Random.get_random_bytes(8)
    block_size = 8

    key = str(key)

    if len(key) % 16 != 0:
        key += ' ' * (16 - len(key) % 16)

    decryptor = DES3.new(key, DES3.MODE_CFB, IV)

    file_ext = file[len(file) - 4:]

    if file_ext != '.enc':
        print 'Please enter the name of an encrypted file; cannot decrypt plaintext'
        return False

    input_filename = file
    output_filename = 'DEC_' + file[:len(file) - 4]

    with open(input_filename, 'rb') as f_input:
        with open(output_filename, 'wb') as f_output:
            while True:
                block = f_input.read(block_size)
                if len(block) == 0:
                    break

                plain_block = decryptor.decrypt(block)
                f_output.write(plain_block)

    return True


