from time import time
from tqdm import tqdm
from random import randint, choice

from utils import Timer
from server import Server
from user import User
import const

# create server and user instances
server = Server()
users = [
    User() 
    for _ in tqdm(range(const.USER_COUNT), desc='Creating Users')
]

# registration stage
for user in tqdm(users, desc='Registration'):
    server.register(user)

# activity simulation
timer = Timer()
spots = [set() for _ in range(const.SPOT_COUNT)]
for user in users:
    user.spot = randint(0, const.SPOT_COUNT - 1)
    spots[user.spot].add(user)

def step():
    for user in users:
        user.timer.tick()
        
        if user.timer.time() % const.STAY_PERIOD == 0:
            # time to leave current spot and choose a random one
            spots[user.spot].remove(user)
            user.spot = randint(0, const.SPOT_COUNT - 1)
            spots[user.spot].add(user)
        
        if user.timer.time() % const.EXCHANGE_PERIOD == user.exchange_time:
            # time to exchange token with nearby users
            other: User
            for other in spots[user.spot]:
                if other != user:
                    token = user.request_token(other)

with tqdm(desc='Simulation', total=const.SIM_DURATION+1) as pbar:
    while timer.time() <= const.SIM_DURATION:
        if timer.time() % 86400 == 0:
            date = timer.time() // 86400

            # initiate daily routine: generate rotating key, etc
            for user in users:
                user.daily_routine()
            
                # upload the tokens got in previous day
                if date > 0:
                    server.upload(user, date - 1)

        step()
        
        pbar.update(1)
        timer.tick()

print(f"""
Simulation done
Duration: {const.SIM_DURATION / 86400} days
Population / Spot Amount: {const.USER_COUNT} / {const.SPOT_COUNT}
Total tokens uploaded: {server.tokensSize()}
""")

begin = time()

infected = choice(users)
contacted = server.report(infected, timer.time() // 86400)
print(f"""
Picking "index case": {infected.id}
""")

for date in sorted(contacted.keys()):
    exposed = contacted[date]
    print(f"Date {date}: {len(exposed)} exposed users found")

print(f"Exposed found in {time() - begin: .4f} seconds")