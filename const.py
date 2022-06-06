# Protocol Parameters
KEY_SIZE=32
ROTATE_COUNT = 16
ROTATE_TIME = 3

EXCHANGE_PERIOD = 5 * 60    # exchange with others every 5 minutes
RANDOM_A_SIZE = 2           # the size of rA (in bytes)
RANDOM_B_SIZE = 16          # the size of rB (in bytes)

INTERACT_LIMIT = 10         # interaction limit per exchange period

# Simulation Parameters
USER_COUNT = 1000
SPOT_COUNT = max(1000, USER_COUNT // 3) # expected each spot has maximum of 10 people
STAY_PERIOD = 3600                      # seconds to stay in each spot  
SIM_DURATION = 86400 * 7                # in seconds