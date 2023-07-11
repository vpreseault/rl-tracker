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

    def addSession(self, date, wins, losses, winrate, games, scores, startMmr, endMmr):
        session = {
            "date": date,
            "chat": True,
            "start_mmr": startMmr,
            "end_mmr": endMmr,
            "wins": wins,
            "losses": losses,
            "winrate": winrate,
            "games": games,
            "scores": scores,
        }
        self.data["s14"]["sessions"].append(session)
        self.updateCurrentMmr(endMmr)
        self.updateWinsLosses(wins, losses)
        self.write()

    def updateCurrentMmr(self, newMmr):
        self.data["s14"]["regular_season"]["current_mmr"] = newMmr

    def updateWinsLosses(self, wins, losses):
        self.data["s14"]["regular_season"]["wins"] += wins
        self.data["s14"]["regular_season"]["losses"] += losses
        self.data["s14"]["regular_season"]["winrate"] = calculateWinrate(
            self.data["s14"]["regular_season"]["wins"],
            (
                self.data["s14"]["regular_season"]["wins"]
                + self.data["s14"]["regular_season"]["losses"]
            ),
        )

    def getCurrentMmr(self):
        return self.data["s14"]["regular_season"]["current_mmr"]
