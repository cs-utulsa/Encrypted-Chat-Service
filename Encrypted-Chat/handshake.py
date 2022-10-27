from curses import keyname


class handshake:  
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
   def handshake(self, socket, boolean):  
        pass

   #ecc method. Takes a socket which is connected, the ecc curve to be used and the secret int that was generated in handshake.   
   #Should use this to create the ECC key and return it once it is done. Only called by the handshake method.
   def ecc(self, socket, secret, curve):  
        pass

   #getkey, returns key. Should delete the key once it has been passed. 
   def getKey(self):  
        temp = key
        del key
        return temp