from datetime import date
import math


class Session:
    def __init__(self, store, startMmr):
        self.store = store

        print(f"Starting MMR: {startMmr}")
        self.startMmr = startMmr
        self.endMmr = startMmr
        self.wins = 0
        self.losses = 0
        self.games = []
        self.scores = []
        self.date = str(date.today())

    def loop(self):
        looping = True
        while looping:
            # quit loop even without two losses
            gameScore = input(f"Game result: ")
            gameResult = self.logGameData(gameScore)

            self.games.append(gameResult)
            if gameResult == -1:
                if self.losses > 1:
                    pitConfirm = ""
                    while pitConfirm != "y" and pitConfirm != "n":
                        pitConfirm = input(
                            "Box. Box. Losses are stacking. End session? (y/n) "
                        )

                    if pitConfirm == "y":
                        looping = False

        self.endSessionDebrief()

    def logGameData(self, score):
        myScore = int(score[0])
        opponentScore = int(score[1])
        self.scores.append({"myScore": myScore, "opponentScore": opponentScore})
        if myScore > opponentScore:
            self.wins += 1
            return 1
        self.losses += 1
        return -1

    def endSessionDebrief(self):
        DASH_FACTOR = 41
        
        gamesPlayed = self.wins + self.losses
        winrate = math.floor(self.wins / gamesPlayed)

        self.endMmr = int(input("What is the ending MMR? "))
        print("-" * DASH_FACTOR)
        print(f"{'-'*3} End of Session Debrief {self.date} {'-'*3}")
        print(f"Games played: \n{gamesPlayed}\n")
        print(f"Wins: {self.wins}, Losses: {self.losses}, winrate: {winrate}%\n")
        print(f"MMR +/-: \n{self.endMmr - self.startMmr}\n")
        input("-" * DASH_FACTOR)

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
