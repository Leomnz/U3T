import games
from games import Game, GameState


TicTacToe = games.TicTacToe()
state = TicTacToe.initial


# play the game
while True:
    print("Possible Actions:", TicTacToe.actions(state))
    move = int(input('Enter your move: '))
    move = TicTacToe.actions(state)[move]
    state = TicTacToe.result(state, move)
    TicTacToe.display(state)
    if TicTacToe.terminal_test(state):
        print('You win!')
        break
    move = games.minmax_player(TicTacToe, state)
    print('My move is:', move)
    state = TicTacToe.result(state, move)
    TicTacToe.display(state)
    if TicTacToe.terminal_test(state):
        print('You lose!')
        break