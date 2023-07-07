from datetime import date
import math


class Session:
    def __init__(self, startMmr):
        print(f"Starting MMR: {startMmr}")
        self.startMmr = startMmr
        self.endMmr = startMmr
        self.games = []
        self.date = date.today()

    def loop(self):
        looping = True
        lossCount = 0
        while looping:
            gameScore = input(f"Game result: ")
            gameResult = self.convertScoreToWinLoss(gameScore)

            self.games.append(gameResult)
            if gameResult == -1:
                lossCount += 1
                if lossCount > 1:
                    pitConfirm = ""
                    while pitConfirm != "y" and pitConfirm != "n":
                        pitConfirm = input(
                            "Box. Box. Losses are stacking. End session? (y/n) "
                        )

                    if pitConfirm == "y":
                        looping = False

        self.endSessionDebrief()

    def convertScoreToWinLoss(self, score):
        myScore = score[0]
        opponentScore = score[1]
        if myScore > opponentScore:
            return 1
        return -1

    def endSessionDebrief(self):
        DASH_FACTOR = 41

        numGames = len(self.games)
        record = sum(self.games)
        winrate = math.floor(
            ((math.floor(numGames / 2) + math.ceil(record / 2)) / numGames) * 100
        )

        self.endMmr = int(input("What is the ending MMR? "))
        print("-" * DASH_FACTOR)
        print(f"{'-'*3} End of Session Debrief {self.date} {'-'*3}")
        print(f"Games played: \n{numGames}\n")
        print(f"Session +/-: \n{record} ({winrate}%)\n")
        print(f"MMR +/-: \n{self.endMmr - self.startMmr}\n")
        print("-" * DASH_FACTOR)
