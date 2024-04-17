from pettingzoo.test import api_test
from sos_environment.env import sos_environment
from pettingzoo.test import max_cycles_test




env = sos_environment.env()

api_test(env, num_cycles=1000, verbose_progress=True)