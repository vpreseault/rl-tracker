import json

from Utility import *


class Store:
    def __init__(self, gamemode):
        file = open("data.json", "r")
        data = json.load(file)
        file.close()
        self.data = data

        self.gamemode = gamemode
        self.regularSeason = self.data["s13"][self.gamemode]["regularSeason"]

    def write(self):
        file = open("data.json", "w")
        json.dump(self.data, file)
        file.close()

    def addSession(self, sessionResult):
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

    def getCurrentMmr(self):
        return self.regularSeason["currentMmr"]
