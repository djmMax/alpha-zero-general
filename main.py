from Coach import Coach
from ultimate_tictactoe.TicTacToeGame import TicTacToeGame
from ultimate_tictactoe.keras.NNet import NNetWrapper as nn
from utils import *

args = dotdict({
    'numIters': 10,
    'numEps': 50,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 25,
    'arenaCompare': 20,
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': False,
    'load_example': True,
    'load_folder_file': ('./temp/','checkpoint-x2.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
})

if __name__=="__main__":
    g = TicTacToeGame()
    nnet = nn(g)

    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], 'best.bak.pth.tar') #args.load_folder_file[1])

    c = Coach(g, nnet, args)
    if args.load_example:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()
