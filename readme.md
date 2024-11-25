
# Knight's Tour Grid Game

A Python game implementing a variation of the Knight's Tour chess puzzle using Pygame.

## Description

This game presents players with a rectangular grid where they must make valid knight moves (as in chess) to visit as many squares as possible. The game features:

- A 5x10 rectangular grid
- Knight movement validation (L-shaped moves: 2 squares in one direction, 1 square perpendicular)
- Visual highlighting of valid moves
- Score tracking and maximum possible moves calculation
- Game over detection when no valid moves remain
- Reset functionality

## Features

- Real-time highlighting of valid moves in green
- Game over state shown in pink
- Move counter display
- Maximum achievable moves calculation using Warnsdorff's algorithm
- Simple controls: mouse clicks for moves, 'R' key to reset

## Requirements

- Python 3.x
- Pygame
- Loguru (for logging)

## Installation

1. Ensure Python 3.x is installed
2. Install required packages:```bash
pip install pygame loguru
```

## How to Play

1. Run the script:
```bash
python main.py
```

2. Game Rules:
   - Click any cell to start
   - Subsequent moves must follow knight's movement pattern (L-shape)
   - Valid moves are highlighted in green
   - Numbers show the sequence of your moves
   - Game ends when no valid moves remain
   - Press 'R' to reset the game at any time

## Technical Details

- Uses Warnsdorff's algorithm to calculate maximum possible moves
- Implements efficient move validation
- Real-time visual feedback for valid moves
- Comprehensive logging system using Loguru
- Type-hinted functions for better code maintainability

## Controls

- Left Mouse Button: Make a move
- R key: Reset game
- Close window to quit

## Game States

- White cells: Unvisited
- Green cells: Valid moves from current position
- Pink background: Game over state
- Numbers: Move sequence

## Performance

The game includes optimization features such as:
- Efficient grid state management
- Pre-calculated maximum possible moves
- Real-time move validation
- Minimal redraw operations
