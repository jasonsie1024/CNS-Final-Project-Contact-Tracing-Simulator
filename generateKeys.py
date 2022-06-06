from Crypto.Hash import keccak, SHA3_512
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
import os

d = 32
t = 2

def hash(data):
    return SHA3_512.new().update(data)

class User:
    def __init__(self, id):
        self.id = id
        self.sk = ECC.generate(curve='NIST P-256')
        self.pk = self.sk.public_key()
        
        # daily updated key
        self.key = os.urandom(d)
    
    def updateKey(self):
        self.key = os.urandom(d)

    def getHashKey(self):
        return hash(self.key + os.urandom(t)).digest()

    def contactWith(self, user):
        k = user.getHashKey()
        hk = hash(k + os.urandom(t))
        rec = (hk.digest().hex(), self.id)
        recHash = hash(hk.digest() + self.id)

        signer = DSS.new(self.sk, 'fips-186-3')
        sig = signer.sign(recHash)

        return rec, sig.hex()

alice = User(b"alice")
bob = User(b"bob")

for _ in range(10):
    print(alice.getHashKey().hex())
    print(alice.contactWith(bob))