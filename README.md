# Clion-ChessEngine

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Instructions](#instructions)
* [Contributing](#contributing)


## General info
Clion is a Chess Engine developed in Python. It is an attempt to develop an Engine which can play at `FIDE` Rating of `2000+` currently it plays aproximately at `1800 ELO`. Current Improvement areas include efficiently calculating moves which can give fruitfull results and hence can be helpful to increase Engine's `DEPTH` of calculating moves.

## Technologies
* Python 3.12.3
* pygame 2.0.1

## Instructions
1. **Clone the Repository**
   ```bash
   git clone https://github.com/ShubhamPhapale/Clion-ChessEngine.git
   ```
2. **Execute command** 
   ```bash
   pip install requirements.txt
   ```
   Note : You may directly use the newenv by activating it
3. **Change directory to `src`**
   ```bash
   cd src
   ```
3. **Execute Command**:
   ```bash
   python ChessMain.py
   ```
Note : You can select Human / AI to play in the ChessMain.py by setting boolean flags for whiteplayer / blackplayer

#### Handling:
* Press `z` to undo a move.
* Press `r` to reset the game.

## Additional Resources

- [YouTube Video](https://youtu.be/Ym0UC2HWFBY)
- [My YouTube Channel](https://www.youtube.com/channel/UCzOmg9hOy3NBsScX--Nrb5Q)

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Added some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
