from functools import partial
import sys
import os

from .smac_hard.env.multiplayer_multiagentenv import MultiPlayer_MultiAgentEnv
from .smac_hard.env.starcraft2.starcraft2 import StarCraft2Env

def env_fn(env, **kwargs) -> MultiPlayer_MultiAgentEnv:
    return env(**kwargs)

REGISTRY = {}
REGISTRY["sc2"] = partial(env_fn, env=StarCraft2Env)

if sys.platform == "linux":
    os.environ.setdefault("SC2PATH", "~/StarCraftII")
