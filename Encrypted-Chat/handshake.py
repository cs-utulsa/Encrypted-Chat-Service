from curses import keyname
import secrets

class Handshake:  
   key = None  
   encryptCurve = 'NIST P-256'  
   gen = None  
   prime = None  
   x = None  
   #Constructor. Takes curve string as argument.  
   def __init__(self, curve):  
        if curve != 'default':  
            encryptCurve = curve  

   #handshake method. Takes a socket which is connected and a boolean. True = sever calling,  
   #false = client calling. returns the socket after finishing the handshake.  
   def handshake(self, socket, isServer):  
        pass

   #ecc method. Takes a socket which is connected, the ecc curve to be used and the secret int that was generated in handshake.   
   #Should use this to create the ECC key and return it once it is done. Only called by the handshake method.
   def ecc(self, secret, curve):
     #gen will contain integer within the range of [0-curve.field.n]
     #[curve.field.n] is all integers within the curve 
     gen = secret.randbelow(curve.field.n)
     return gen

   #getkey, returns key. Should delete the key once it has been passed. 
   def getKey(self):  
        temp = key
        del key
        return temp