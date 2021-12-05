# NEAT NewOldStarCreft
## Building an Intelligent Agent for a video game using NEAT

In this project I apply an algorithm called NEAT, also known as NeuroEvolution of Augmenting Topologies, to a video game developed with Pygame, in an attempt to train an AI to control the spaceship player character and excel at the game.

The goal of the game is to dodge incoming enemy aliens while collecting as many planets, asteroids and whatnot as possible, scoring different amounts of points in doing so.

For more info on NEAT, visit https://neat-python.readthedocs.io/en/latest/neat_overview.html to review documentation.

*This is a university assignment and a learning project for me, thus the results may vary.*

## The original game

The original game was developed by [@RikuVirtanen](https://github.com/RikuVirtanen) and its source code can be found in this [NewOldStarCreft repo](https://github.com/RikuVirtanen/NewOldStarCreft).

[Riku's](https://github.com/RikuVirtanen) original game is a bit more complex, with the player having the ability to move sideways as well as up and down, and the enemy aliens also moving at randomized speeds. For the sake of the university assignment and an "easier" environment for the intelligent agent to learn, I have made a somewhat simplified and essentially a "dumbed-down" version of the game, in which all the enemy aliens move at a constant speed and the player(s) can only move up and down. Additionally, the player(s) will die as soon as they hit an enemy, whereas in the original game the player starts with 3 lives.