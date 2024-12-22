from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import setup

description = """SMAC-HARD - SMAC-Hard: Enabling Mixed Opponent Strategy Script and Self-play on SMAC

SMAC offers a diverse set of decentralised micromanagement challenges based on
StarCraft II game. In these challenges, each of the units is controlled by an
independent, learning agent that has to act based only on local observations,
while the opponent's units are controlled by the built-in StarCraft II AI.

The accompanying paper which outlines the motivation for using SMAC as well as
results using the state-of-the-art deep multi-agent reinforcement learning
algorithms can be found at https://www.arxiv.link

Read the README at https://github.com/oxwhirl/smac for more information.
"""

extras_deps = {
    "dev": [
        "pre-commit>=2.0.1",
        "black>=19.10b0",
        "flake8>=3.7",
        "flake8-bugbear>=20.1",
    ],
}


setup(
    name="SMAC-HARD",
    version="1.0.0",
    description="SMAC-HARD - SMAC-Hard: Enabling Mixed Opponent Strategy Script and Self-play on SMAC.",
    long_description=description,
    author="DevinDeng",
    author_email="devindeng@zju.edu.cn",
    license="MIT License",
    keywords="StarCraft, SMAC, SMAC-HARD",
    url="https://github.com/devindeng94/hard-smac",
    packages=[
        "smac_hard",
        "smac_hard.env",
        "smac_hard.env.starcraft2",
        "smac_hard.env.starcraft2.maps",
        "smac_hard.bin",
    ],
    extras_require=extras_deps,
    install_requires=[
        "protobuf<3.21",
        "pysc2>=3.0.0",
        "s2clientprotocol>=4.10.1.75800.0",
        "absl-py>=0.1.0",
        "numpy>=1.10",
        "pygame>=2.0.0",
    ],
)