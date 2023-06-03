i = 0
while i <= 5:
    print(i)
    i += 1
    
key gen
import cryptography 
from cryptography.fernet import Fernet   
key = Fernet.generate_key()
with open("symmetric.key", "wb") as fo:
            fo.write(key)