import math
import json


def calculateWinrate(wins, totalGames):
    return math.floor((wins / totalGames) * 100)


def getRankDistribution():
    file = open("rankDistribution.json", "r")
    data = json.load(file)
    file.close()
    return data
