import json

class Store:
    def __init__(self):
        file = open('data.json', 'r')
        data = json.load(file)
        file.close()
        self.data = data

    def write(self):
        file = open('data.json', 'w')
        json.dump(self.data, file)
        file.close()

    def addSession(self, date, games, startMmr, endMmr):
        session = {"date": date, "games": games, "start_mmr": startMmr, "end_mmr": endMmr}
        self.data["s14"]["sessions"].append(session)
        self.updateCurrentMmr(endMmr)
        self.updateWinsLosses(games)
        self.write()

    def updateCurrentMmr(self, newMmr):
        self.data["s14"]["regular_season"]["current_mmr"] = newMmr

    def updateWinsLosses(self, newGames):
        winCount = 0
        lossCount = 0
        for result in newGames:
            if result == 1:
                winCount += 1
            else:
                lossCount += 1
        
        self.data["s14"]["regular_season"]["wins"] += winCount
        self.data["s14"]["regular_season"]["losses"] += lossCount

    def getCurrentMmr(self):
        return self.data["s14"]["regular_season"]["current_mmr"]
