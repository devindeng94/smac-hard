# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Define the mini game map configs. These are maps made by Deepmind."""

from pysc2.maps import lib


class MiniGame(lib.Map):
  directory = "pysc2_maps"
  download = "https://github.com/deepmind/pysc2#get-the-maps"
  players = 1
  score_index = 0
  game_steps_per_episode = 0
  step_mul = 8


mini_games = [
    "3m",
    "3m_modified"
]


for name in mini_games:
  globals()[name] = type(name, (MiniGame,), dict(filename=name))
