# Use pytest and comment your code: https://docs.pytest.org/en/7.2.x/
from Crypto import Random
import unittest
import os, os.path
from os.path import exists

from crypto.encrypt import ECEncrypt

class test(unittest.TestCase):
    key = Random.new().read(16)
    enc = ECEncrypt(key,key)

    def encryptsMessage(self):
        """KS Unit Test 1: Verifies that the text is being manipulated and does not remain as plaintext""" 
        result = self.enc.encrypt("test")
        original = "test"
        print(original)
        self.assertNotEqual(result, original)

    def decryptsMessage(self):
        """KS Unit Test 2: Verifies that the text is being decrypted correctly"""
        encryptMsg = ECEncrypt.encrypt("test")
        decryptMsg = ECEncrypt.decrypt(encryptMsg)
        original = "test"
        self.assertEqual(decryptMsg, original)  

    def unpadMessage(self):
        """KS Unit Test 3: Verifies that the padding is being removed - WIP"""
        testTxt = "test"
        padData = ECEncrypt._pad(testTxt.decode('utf8'))
        result = ECEncrypt.unpad(padData[16:])
        self.assertEqual(testTxt, result)

if __name__ == '__main__':
    unittest.main()
