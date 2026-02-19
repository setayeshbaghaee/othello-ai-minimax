## Othello AI – Minimax with Alpha-Beta Pruning
## 📌 Project Overview

This project is a Python implementation of the classic board game Othello (Reversi) with a graphical interface and an AI opponent powered by the Minimax algorithm enhanced with Alpha-Beta pruning.

I built this project to better understand adversarial search algorithms and to implement a complete game system from scratch — including board logic, move validation, and AI decision-making.

The result is a fully playable Human vs AI game with adjustable difficulty.

## Project Objectives

Implement the complete rules and mechanics of Othello

Design an interactive graphical interface using Tkinter

Build an AI opponent using Minimax

Optimize search performance with Alpha-Beta pruning

Practice recursive algorithm design and game-tree reasoning

## AI Implementation
Minimax Algorithm

The AI simulates future game states up to a configurable depth and selects the move that maximizes its score, assuming the opponent also plays optimally.

This required:

Recursive state evaluation

Alternating maximizing/minimizing layers

Careful board copying to avoid state corruption

Alpha-Beta Pruning

To improve performance, Alpha-Beta pruning eliminates branches of the search tree that cannot influence the final decision.

This significantly reduces computation time and allows deeper search levels without exponential slowdown.

Evaluation Function

The board is evaluated based on:

Difference between black and white discs

Perspective of the AI player

Although simple, this heuristic provides reasonable gameplay performance.
(See “Future Improvements” for enhancements.)

## Game Features

Fully functional 8×8 Othello board

Legal move detection in all 8 directions

Automatic disc flipping according to official rules

Human vs AI gameplay

Adjustable AI search depth

Game-over detection with winner announcement

Highlighting of valid moves

Clean Tkinter-based GUI

## Repository Structure
```bash

othello-ai-minimax/
│
├── eothello.py        # Main game implementation
├── eothello.ipynb     # Step-by-step explanation of algorithm logic
├── main page.png      # Screenshot of the interface
└── README.md
```
## ▶️ How to Run

Clone the repository:

git clone https://github.com/setayeshbaghaee/othello-ai-minimax.git
cd othello-ai-minimax


Make sure Python 3.8+ is installed, then run:

python eothello.py


The game window will open and you can start playing against the AI.

## What I Learned

Through this project, I improved my understanding of:

Implementing board game logic from scratch

Designing recursive adversarial algorithms

Managing game state transitions safely

Applying Alpha-Beta pruning for performance optimization

Integrating algorithmic computation with a GUI system

This project helped me bridge theoretical AI concepts with practical implementation.

## Future Improvements

Improve evaluation function (positional weights, corner prioritization)

Implement move ordering to enhance pruning efficiency

Add multiple difficulty levels

Track game statistics

Improve UI styling and animations

📸 Screenshot

(See main page.png in the repository.)

## Conclusion

This project combines recursion, algorithm design, and GUI development into a complete playable application.

It demonstrates practical implementation of adversarial search algorithms in a competitive two-player environment.


---

## 📌 Author

Setayesh Baghaee
Computer Engineering Student
