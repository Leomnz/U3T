## Ultimate Tic-Tac-Toe AI
This project is an implementation of Minimax, Alpha-beta, Random player and MCTS for ultimate Tic-Tac-Toe. 
This project uses the standard ruleset defined on wikipedia where after a box is won it can no longer be played in.

### Installation
```bash
git clone https://github.com/Leomnz/U3T
cd U3T
wget https://raw.githubusercontent.com/aimacode/aima-python/master/games.py
wget https://raw.githubusercontent.com/aimacode/aima-python/master/games4e.py
```
Alternatively drop this repository into the https://github.com/aimacode/aima-python directory

### Algorithm Win-Rate
![Winrate Table](https://github.com/Leomnz/U3T/blob/463698911bd55add2b51557ca031e01cef5ed7d0/tablev3.png?raw=true)

This table shows the win rate for each algorithm match up (excluding draws), with blue
representing a higher win rate and red representing a lower win rate. So To see the win rate of alpha-beta pruning against MCTS
you would look at the second column, third row to find that it is 0.166 meaning that alpha-beta won approximately 17% of the non-draw games.
