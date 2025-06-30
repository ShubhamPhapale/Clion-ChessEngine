# Chess Engine

A Python chess engine with a graphical interface built using Pygame. The engine features a modular design, an AI player that plays at approximately 1800 ELO rating, and supports standard chess rules including castling, en passant, and pawn promotion.

## Features

- Full implementation of chess rules
- Graphical user interface with piece movement animation
- AI opponent using alpha-beta pruning search
- Support for:
  - Castling (kingside and queenside)
  - En passant captures
  - Pawn promotion
  - Threefold repetition detection
  - Fifty-move rule
- Move validation and legal move highlighting
- Game state tracking (checkmate, stalemate, draws)
- Undo move functionality

## Project Structure

```
src/
  ├── core/           # Core game logic
  │   ├── game_state.py
  │   ├── move.py
  │   └── castle_rights.py
  ├── ai/             # AI player implementation
  │   ├── engine.py
  │   └── evaluator.py
  ├── ui/             # User interface
  │   └── game_ui.py
  ├── utils/          # Utility functions
  │   ├── constants.py
  │   └── fen.py
  └── main.py         # Main game entry point
```

## Requirements

- Python 3.12+
- Pygame
- python-chess

Install dependencies using:
```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository
2. Install dependencies
3. Run the game:
```bash
python src/main.py
```

## Controls

- Mouse: Click and drag pieces to move them
- 'z': Undo last move
- 'r': Reset game
- Close window to quit

## AI Features

The AI player uses several techniques to play strong chess:

- Alpha-beta pruning search
- Position evaluation using:
  - Material counting
  - Piece-square tables
  - Mobility evaluation
  - King safety assessment
- Endgame detection and specialized evaluation
- Move ordering for better pruning

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
