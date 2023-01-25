from Crypto import Random
from Crypto.Cipher import AES

class ECEncrypt:
    """
    ekey = encryption key
    dkey = decryption key 
    """
    def __init__(self, ekey, dkey):
        self.AES_EKEY = ekey
        self.AES_DKEY = dkey

    """
    Setter for Encryption key
    """
    def set_enc_key(self, key:bytes):
        self.AES_EKEY = key

    """
    Setter for Decryption key
    """
    def set_dec_key(self, key:bytes):
        self.AES_DKEY = key

    """
    Encrypt the data and retrun the encrypted data
    """
    def encrypt(self, data:str):
        data = self._pad(data.decode('utf8'))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.AES_EKEY, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(data.encode('utf8'))
    
    """
    Decrypt the bytes with the key and call the unpad method
    """
    def decrypt(self, data:bytes):
        iv = data[:16]
        decrypt_cipher = AES.new(self.AES_DKEY, AES.MODE_CBC, iv)
        return self.unpad(decrypt_cipher.decrypt(data[16:]).decode('utf8'))

    """
    Pad the data to achieve equivalent blocksize
    """
    def _pad(self, s):
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

    """
    Unpad the data
    """
    def unpad(self, data):
        return data[:-ord(data[-1])]