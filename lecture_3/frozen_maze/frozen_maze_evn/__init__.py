import os
from gym.envs.registration import register

# Allowing environment to have sounds
if "SDL_AUDIODRIVER" in os.environ:
    del os.environ["SDL_AUDIODRIVER"]

register(
    id="FrozenMaze-v0",
    entry_point='frozen_maze_evn.frozen_maze:FrozenMazeEnv'
)
