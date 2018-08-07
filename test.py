from ultimate_tictactoe.TicTacToeGame import TicTacToeGame, display
from ultimate_tictactoe.TicTacToePlayers import *
import Arena
g = TicTacToeGame()

rp = RandomPlayer(g).play
hp = HumanTicTacToePlayer(g).play
arena = Arena.Arena(hp, hp, g, display=display)
print(arena.playGames(2, verbose=True))