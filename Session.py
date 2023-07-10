from datetime import date
import math
import json



class Session:
    def __init__(self, store, startMmr):
        self.store = store

        print(f"Starting MMR: {startMmr}")
        self.startMmr = startMmr
        self.endMmr = startMmr
        self.currentMmr = startMmr
        self.mmrFactor = 9

        file = open("rankDistribution.json", "r")
        data = json.load(file)
        file.close()
        self.rankDistribution = data
        self.startingRank = self.calculateRank(startMmr)

        self.wins = 0
        self.losses = 0
        self.games = []
        self.scores = []
        self.date = str(date.today())

    def loop(self):
        looping = True
        while looping:
            while True:
                gameScore = input(f"Game result: ").strip()
                if self.gameResultInputIsSafe(gameScore):
                    break

                print("Please enter valid game score (Format ##).")   

            if gameScore == "q":
                looping = False
            else:
                myScore, opponentScore = self.seperateToIndividualScores(gameScore)
                self.scores.append({"myScore": myScore, "opponentScore": opponentScore})

                gameResult = self.checkWin(myScore, opponentScore)
                self.games.append(gameResult)

                if gameResult == 1:
                    self.wins += 1
                    self.currentMmr += self.mmrFactor
                    self.checkRankChange(self.currentMmr)
                else:
                    self.losses += 1
                    self.currentMmr -= self.mmrFactor

                    if self.losses > 1:
                        stopSessionInput = ""
                        while stopSessionInput != "y" and stopSessionInput != "n":
                            stopSessionInput = input(
                                "Box. Box. Losses are stacking. End session? (y/n) "
                            ).strip()

                        if stopSessionInput == "y":
                            looping = False

        gamesPlayed = self.wins + self.losses
        winrate = math.floor((self.wins / gamesPlayed)*100)
        self.endSessionDebrief(gamesPlayed, winrate)
        self.store.addSession(
            self.date,
            self.wins,
            self.losses,
            winrate,
            self.games,
            self.scores,
            self.startMmr,
            self.endMmr,
        )

    def seperateToIndividualScores(self, input):
        return int(input[0]), int(input[1])

    def checkWin(self, myScore, opponentScore):
        if myScore > opponentScore:
            return 1        
        return -1

    def endSessionDebrief(self, gamesPlayed, winrate):
        DASH_FACTOR = 41

        # validate input
        self.endMmr = int(input("What is the ending MMR? ").strip())
        print("-" * DASH_FACTOR)
        print(f"{'-'*3} End of Session Debrief {self.date} {'-'*3}")
        print(f"Games played: \n{gamesPlayed}\n")
        print(f"Wins: {self.wins}, Losses: {self.losses}, winrate: {winrate}%\n")
        print(f"MMR +/-: \n{self.endMmr - self.startMmr}\n")
        input("-" * DASH_FACTOR)

    def calculateRank(self, mmr):
        for rank in reversed(self.rankDistribution):
            if (mmr < self.rankDistribution[rank]["promotion"] and mmr > self.rankDistribution[rank]["demotion"]):
                return rank


    def checkRankChange(self, currentMmr):
        currentRank = self.calculateRank(currentMmr)
        # print message if rank has changed and it has increased (no message for demotions)
        if currentRank != self.startingRank and self.currentMmr > self.startMmr:
            self.calculateRank = currentRank
            print(f"That's {currentRank}! Well done mate.")

    def gameResultInputIsSafe(self, input):
        # accepted values: q, ##
        if input.isdigit() and len(input) == 2:
            # two digit number confirmed
            return True
        elif input == "q":
            # exit command confirmed
            return True
        return False