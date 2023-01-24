from environment.two_armed_bandit_env import TwoArmedBanditEnv
from gym.envs.registration import register

register(
    id="TwoArmedBanditEnv-v1",
    entry_point="environment.two_armed_bandit_env:TwoArmedBanditEnv"
)

(TwoArmedBanditEnv,)
