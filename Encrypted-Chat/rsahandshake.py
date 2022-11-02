import socket
import rsa
from Crypto import Random
class RSAHandshake:  
     def __init__(self):
          self.publicKey, self.privateKey = rsa.newkeys(1024)
          self.ekey = Random.new().read(16)
     

     def handshake(self, csock=None, srv=None): 
          if srv == None:
               print("Client Handshake")
               # RECV PUB KEY
               spubkey = rsa.PublicKey._load_pkcs1_der(csock.recv(2048))

               # SEND PUB KEY AND ENCRYPTED AES KEY
               data = self.publicKey._save_pkcs1_der() + rsa.encrypt(self.ekey, spubkey)
               csock.sendall(data)
               # RECV SERVER AES KEY
               ckey = rsa.decrypt(csock.recv(2048), self.privateKey)
               print("Done")
               print(f'MYKEY: {self.ekey} OTHER KEY: {ckey}')
               return self.ekey, ckey
          else:
               print("Server Handshake")
               # SEND PUB KEY
               csock.sendall(self.publicKey._save_pkcs1_der())
               # RECV PUB KEY AND ENCRYPTED AES KEY
               data = csock.recv(2048)
               cpubkey = rsa.PublicKey._load_pkcs1_der(data[:140])
               ckey = rsa.decrypt(data[140:], self.privateKey)
               # SEND AES KEY TO CLIENT
               csock.sendall(rsa.encrypt(self.ekey, cpubkey))
               print("Done")
               print(f'MYKEY: {self.ekey} OTHER KEY: {ckey}')
               return self.ekey, ckey