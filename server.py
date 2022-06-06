from __future__ import annotations
from dataclasses import dataclass, field
from random import shuffle

from utils import id, verify, genKey, ECC, H
from user import User

@dataclass
class Server:
    # {userId: userPk}
    __userPk: dict[str, ECC.EccKey] = field(default_factory=lambda: {})
    # {userId: {date: set(tokens)}}
    __userTokens: dict[str, dict[int, ]] = field(default_factory=lambda: {})
    # {token: (user, date)}
    __tokens: dict[str, tuple[User, int]] = field(default_factory=lambda: {})

    def __post_init__(self):
        self.__sk, self.pk = genKey()

    def register(self, user: User):
        # simplified registeration
        # require more detailed authentication implementation!

        uid = id()
        while uid in self.__userPk.keys(): uid = id()
        try:
            verify(user.pk, uid, user.auth(uid))
        except ValueError:
            raise Exception("User can't prove pocess of correspond sk")

        user.id = uid
        self.__userPk[user.id] = user.pk

    def upload(self, user: User, date: int):
        # verify user identity first
        try:
            verify(self.__userPk[user.id], user.id, user.auth(user.id))
        except ValueError:
            raise Exception("User can't prove identity'")

        for token in user.tokens[date].keys():
            self.__tokens[token] = (user, date)

    def report(self, user: User, date: int):
        keys = user.report_keys(date)
        contacted = dict()
        for (k, ra, rb) in keys:
            token = H(H(k + ra + rb) + rb)
            exposed, date = self.__tokens.get(token, (None, 0))
            if exposed is not None:
                if date not in contacted.keys(): contacted[date] = set()
                exposed.verify(date, (k, ra, rb))
                contacted[date].add(exposed)
        return contacted

    def tokensSize(self):
        return len(self.__tokens)
