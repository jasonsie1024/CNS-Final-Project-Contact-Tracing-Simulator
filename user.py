from __future__ import annotations
from dataclasses import dataclass, field

from utils import H, R, genKey, sign, Timer
from random import randint, shuffle
import const

@dataclass
class User:
    id: str = field(default_factory=lambda: R(16))
    active: bool = field(default=True)
    key: str = field(default=None)
    timer: Timer = field(default_factory=lambda: Timer())
    spot: int = field(default=None)

    # tokens = {date: {token: r}}
    tokens: dict[int, dict[str, str]] = field(default_factory=lambda: {})
    # keys = {date: [(key, ra, rb)]}
    __keys: dict[int, list[tuple[str, str, str]]] = field(default_factory=lambda: {})

    def __post_init__(self):
        self.__sk, self.pk = genKey()
        self.exchange_time = randint(0, const.EXCHANGE_PERIOD - 1)
    
    def __hash__(self):
        return int(self.id, 16)
    
    def __eq__(self, other: User):
        return self.id == other.id

    def auth(self, id: str):
        return sign(self.__sk, id)

    def daily_routine(self):
        self.key = R(const.KEY_SIZE)
        self.rotate_keys = [H(self.key + str(i)) for i in range(10)]
        shuffle(self.rotate_keys)

    def store_token(self, token: str, r: str):
        date = self.timer.time() // 86400
        if date not in self.tokens.keys():
            self.tokens[date] = dict()
        
        self.tokens[date][token] = r

    def request_token(self, u: User):
        rb = R(const.RANDOM_B_SIZE)
        intermediate_token = u.reply_token(rb)
        token = H(intermediate_token + rb)

        self.store_token(token, rb)

        return token

    def store_keys(self, keys: tuple[str, str, str]):
        date = self.timer.time() // 86400
        if date not in self.__keys.keys():
            self.__keys[date] = []
        self.__keys[date].append(keys)

    def reply_token(self, r: str):
        ra = R(const.RANDOM_A_SIZE)

        t = (self.timer.time() % 86400) // (const.ROTATE_COUNT * const.ROTATE_TIME)
        rotate_key = self.rotate_keys[t % len(self.rotate_keys)]

        self.store_keys((rotate_key, ra, r))

        intermediate_token = H(rotate_key + ra + r)
        return intermediate_token

    def report_keys(self, date):
        res = []
        for d in range(date - 14, date):
            if d in self.__keys.keys():
                res += self.__keys[d]
        
        shuffle(res)
        return res

    def verify(self, date: int, keys: tuple[str, str, str]):
        k, ra, rb = keys
        token = H(H(k + ra + rb) + rb)

        if (token not in self.tokens[date]) or (self.tokens[date][token] != rb):
            raise Exception("Wrongful Quarantine! 😤😤")


