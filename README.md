## Ultimate Tic-Tac-Toe AI
This project contains random movement, minimax with alpha-beta pruning, heat mapping, and Monte-Carlo Tree Search agents for Ultimate Tic-Tac-Toe. 
This project uses the standard U3T ruleset defined on wikipedia. Particularly, it is important to note that after a grid has been won by a player, no moves can be played in the grid.

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
representing a higher win rate and red representing a lower win rate. So, to see the win rate of alpha-beta pruning against MCTS
you would look at the second column, third row to find that it is 0.166. In other words, alpha-beta pruning won approximately 17% of the non-draw games.

### Full Experimental Discussion
A PDF containing a full experimental discussion of the project is attached below.

[Ultimate Tic Tac Toe Artificial Intelligence Agents.pdf](https://github.com/Leomnz/U3T/files/15138620/Ultimate.Tic.Tac.Toe.Artificial.Intelligence.Agents.pdf)
