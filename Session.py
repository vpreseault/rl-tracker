from datetime import date

from Utility import *


class Session:
    def __init__(self, startMmr):
        self.date = str(date.today())

        print(f"Starting MMR: {startMmr}")
        self.startMmr = startMmr
        self.endMmr = startMmr
        self.currentMmr = startMmr
        self.mmrFactor = 9
        self.estimatedMmr = []

        self.rankDistribution = getRankDistribution()
        self.startingRank = self.calculateRank(startMmr)

        self.wins = 0
        self.losses = 0
        self.games = []
        self.scores = []

    def loop(self):
        looping = True
        while looping:
            gameScore = self.getGameScoreInput()

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

                self.estimatedMmr.append(self.currentMmr)

        gamesPlayed = self.wins + self.losses
        winrate = calculateWinrate(self.wins, gamesPlayed)
        self.endSessionDebrief(gamesPlayed, winrate)
        return {
            "date": self.date,
            "chat": True,
            "startMmr": self.startMmr,
            "endMmr": self.endMmr,
            "estimatedMmr": self.estimatedMmr,
            "wins": self.wins,
            "losses": self.losses,
            "winrate": winrate,
            "games": self.games,
            "scores": self.scores,
        }

    def seperateToIndividualScores(self, input):
        return int(input[0]), int(input[1])

    def checkWin(self, myScore, opponentScore):
        if myScore > opponentScore:
            return 1
        return -1

    def endSessionDebrief(self, gamesPlayed, winrate):
        DASH_FACTOR = 41

        # TODO validate input
        self.endMmr = int(input("What is the ending MMR? ").strip())
        print("-" * DASH_FACTOR)
        print(f"{'-'*3} End of Session Debrief {self.date} {'-'*3}")
        print(f"Games played: \n{gamesPlayed}\n")
        print(f"Wins: {self.wins}, Losses: {self.losses}, winrate: {winrate}%\n")
        print(f"MMR +/-: \n{self.endMmr - self.startMmr}\n")
        input("-" * DASH_FACTOR)

    def calculateRank(self, mmr):
        for rank in reversed(self.rankDistribution):
            if (
                mmr < self.rankDistribution[rank]["promotion"]
                and mmr > self.rankDistribution[rank]["demotion"]
            ):
                return rank

    def checkRankChange(self, currentMmr):
        currentRank = self.calculateRank(currentMmr)
        # print message if rank has changed and it has increased (no message for demotions)
        if currentRank != self.startingRank and self.currentMmr > self.startMmr:
            self.calculateRank = currentRank
            print(f"That's {currentRank}! Well done mate.")

    def editLastScoreInput(self):
        print("Re-enter last game's result.")
        gameScore = self.getGameScoreInput()
        myScore, opponentScore = self.seperateToIndividualScores(gameScore)
        self.scores[-1]["myScore"] = myScore
        self.scores[-1]["opponentScore"] = opponentScore

    def getGameScoreInput(self):
        while True:
            gameScore = input(f"Game result: ").strip()
            if self.gameResultInputIsSafe(gameScore):
                return gameScore

    def gameResultInputIsSafe(self, input):
        # accepted values: q, e, ##
        if input.isdigit() and len(input) == 2:
            # two digit number confirmed
            return True
        elif input == "q":
            # exit command confirmed
            return True
        elif input == "e":
            self.editLastScoreInput()
            return False

        print("Please enter valid game score (Format ##).")
        return False
