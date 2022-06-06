from dataclasses import dataclass, field
from Crypto.Hash import SHA256 as hash
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

from os import urandom
from uuid import uuid4 as uuid

@dataclass
class Timer():
    __time: int = field(default=0)
    def time(self):
        return self.__time
    def tick(self):
        self.__time += 1
        return self.__time

def H(data: str):
    h = hash.new()
    h.update(data.encode('ascii'))
    return h.hexdigest()

def R(size: int):
    return urandom(size).hex()

def id():
    return uuid().hex

def genKey():
    sk = ECC.generate(curve='NIST P-256')
    pk = sk.public_key()
    return (sk, pk)

def sighash(msg: str):
    h = hash.new()
    h.update(msg.encode('ascii'))
    return h

def sign(sk: ECC.EccKey, msg: str):
    signer = DSS.new(sk, 'fips-186-3')
    return signer.sign(sighash(msg))

def verify(pk: ECC.EccKey, msg: str, sig: bytes):
    signer = DSS.new(pk, 'fips-186-3')
    return signer.verify(sighash(msg), sig)