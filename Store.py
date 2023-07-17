import json

from Utility import *


class Store:
    def __init__(self, gamemode):
        file = open("data.json", "r")
        data = json.load(file)
        file.close()
        self.data = data

        self.gamemode = gamemode

    def write(self):
        file = open("data.json", "w")
        json.dump(self.data, file)
        file.close()

    def addSession(self, sessionResult):
        self.data["s14"][self.gamemode]["sessions"].append(sessionResult)
        self.updateCurrentMmr(sessionResult["endMmr"])
        self.updateWinsLosses(sessionResult["wins"], sessionResult["losses"])
        self.write()

    def updateCurrentMmr(self, newMmr):
        self.data["s14"][self.gamemode]["regularSeason"]["currentMmr"] = newMmr

    def updateWinsLosses(self, wins, losses):
        self.data["s14"][self.gamemode]["regularSeason"]["wins"] += wins
        self.data["s14"][self.gamemode]["regularSeason"]["losses"] += losses
        self.data["s14"][self.gamemode]["regularSeason"]["winrate"] = calculateWinrate(
            self.data["s14"][self.gamemode]["regularSeason"]["wins"],
            (
                self.data["s14"][self.gamemode]["regularSeason"]["wins"]
                + self.data["s14"][self.gamemode]["regularSeason"]["losses"]
            ),
        )

    def getCurrentMmr(self):
        return self.data["s14"][self.gamemode]["regularSeason"]["currentMmr"]
