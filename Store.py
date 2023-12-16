import json

from Utility import *


class Store:
    def __init__(self, gamemode):
        file = open("data.json", "r")
        data = json.load(file)
        file.close()
        self.data = data
        self.gamemode = gamemode

        self.regularSeason = data["s13"][gamemode]["regularSeason"]
        self.placements = data["s13"][gamemode]["placements"]

    def write(self):
        file = open("data.json", "w")
        json.dump(self.data, file)
        file.close()

    def addSession(self, sessionResult):
        if self.placements["completed"] == False:
            self.updatePlacements(sessionResult)

        self.data["s13"][self.gamemode]["sessions"].append(sessionResult)

        self.updateCurrentMmr(sessionResult["endMmr"])
        self.updateWinsLosses(sessionResult["wins"], sessionResult["losses"])

        self.write()

    def updateCurrentMmr(self, newMmr):
        self.regularSeason["currentMmr"] = newMmr

    def updateWinsLosses(self, wins, losses):
        self.regularSeason["wins"] += wins
        self.regularSeason["losses"] += losses
        self.regularSeason["winrate"] = calculateWinrate(
            self.regularSeason["wins"],
            (self.regularSeason["wins"] + self.regularSeason["losses"]),
        )

    def updatePlacements(self, sessionResult):
        placementGames = self.placements["games"]
        sessionGames = sessionResult["games"]

        placementScores = self.placements["scores"]
        sessionScores = sessionResult["scores"]

        gamesLeft = 10 - len(placementGames)

        for i in range(0, gamesLeft):
            if i < len(sessionGames):
                placementGames.append(sessionGames[i])
                placementScores.append(sessionScores[i])

        gamesLeft = 10 - len(placementGames)
        if gamesLeft == 0:
            self.placements["completed"] = True
            self.completePlacementStats()

    def completePlacementStats(self):
        wins = 0
        losses = 0
        games = self.placements["games"]

        for game in games:
            if game == -1:
                losses += 1
            elif game == 1:
                wins += 1

        winrate = calculateWinrate(wins, 10)

        self.placements["wins"] = wins
        self.placements["losses"] = losses
        self.placements["winrate"] = winrate

    def getCurrentMmr(self):
        return self.regularSeason["currentMmr"]
