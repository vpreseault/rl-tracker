import json

from Utility import *


class Store:
    def __init__(self):
        file = open("data.json", "r")
        data = json.load(file)
        file.close()
        self.data = data

    def write(self):
        file = open("data.json", "w")
        json.dump(self.data, file)
        file.close()

    def addSession(self, sessionResult):
        self.data["s14"]["sessions"].append(sessionResult)
        self.updateCurrentMmr(sessionResult["endMmr"])
        self.updateWinsLosses(sessionResult["wins"], sessionResult["losses"])
        self.write()

    def updateCurrentMmr(self, newMmr):
        self.data["s14"]["regularSeason"]["currentMmr"] = newMmr

    def updateWinsLosses(self, wins, losses):
        self.data["s14"]["regularSeason"]["wins"] += wins
        self.data["s14"]["regularSeason"]["losses"] += losses
        self.data["s14"]["regularSeason"]["winrate"] = calculateWinrate(
            self.data["s14"]["regularSeason"]["wins"],
            (
                self.data["s14"]["regularSeason"]["wins"]
                + self.data["s14"]["regularSeason"]["losses"]
            ),
        )

    def getCurrentMmr(self):
        return self.data["s14"]["regularSeason"]["currentMmr"]
