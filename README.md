# Clion-ChessEngine

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Instructions](#instructions)


## General info
Clion is a Chess Engine developed in Python. It is an attempt to develop an Engine which can play at `FIDE Rating of` `1500`. Current Improvement areas include efficiently calculating moves which can give fruitfull results and hence can be helpful to increase Engine's `DEPTH` of calculating moves.

## Technologies
* Python 3.12.3
* pygame 2.0.1

## Essentials remaining
- [ ] Draw by three Fold Repetition or by 50 moves rule

## Instructions
1. Clone this repository.
2. Execute command `pip install requirements.txt`
3. Change directory to `src` by executing `cd src`
3. Execute Command `python ChessMain.py`
4. Note : You can select Human / AI to play in the ChessMain.py by setting boolean flags for whiteplayer / blackplayer

#### Handling:
* Press `z` to undo a move.
* Press `r` to reset the game.
