import math


def calculateWinrate(wins, totalGames):
    return math.floor((wins / totalGames) * 100)
