import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import copy

import json

file = open("data.json", "r")
data = json.load(file)
file.close()


def eloOverSeason():
    numberOfSessions = 0

    plotData = {"elo": [], "sessionNumber": []}

    for session in data["s10"]["doubles"]["sessions"]:
        for elo in session["estimatedMmr"]:
            plotData["elo"].append(elo)
            numberOfSessions += 1
    plotData["sessionNumber"] = list(range(1, numberOfSessions + 1))

    return plotData


def resultsAfter3Games():
    plotData = {"results": ["3L", "2L W1", "1L 2W", "3W"], "occurences": [0, 0, 0, 0]}
    for session in data["s10"]["doubles"]["sessions"]:
        if len(session["games"]) > 2:
            print(session["games"])
            r = sum(session["games"][:3])
            if r == -3:
                plotData["occurences"][0] += 1
            elif r == -1:
                plotData["occurences"][1] += 1
            elif r == 1:
                plotData["occurences"][2] += 1
            elif r == 3:
                plotData["occurences"][3] += 1
    return plotData


def chatNoChat():
    plotData = {"results": ["chat", "no chat"], "occurences": [0, 0]}
    for session in data["s10"]["doubles"]["sessions"]:
        if session["chat"]:
            plotData["occurences"][0] += 1
        else:
            plotData["occurences"][1] += 1
    return plotData


def scoreOccurence():
    plotData = {
        "result": [],
        "team": [],
        "occurences": [],
    }
    for i in range(0, 20):
        plotData["occurences"].append(0)
        plotData["result"].append(i // 2)

        if i % 2 == 0:
            plotData["team"].append("Friendly")
        else:
            plotData["team"].append("Enemy")

    for session in data["s10"]["doubles"]["sessions"]:
        try:
            if session["scores"]:
                for game in session["scores"]:
                    fIndex = plotData["result"].index(game["myScore"])
                    eIndex = plotData["result"].index(game["opponentScore"]) + 1

                    plotData["occurences"][fIndex] += 1
                    plotData["occurences"][eIndex] += 1

        except Exception as e:
            print(e)

    df = pd.DataFrame(plotData)
    sns.set_theme(style="whitegrid")
    sns.catplot(
        data=df,
        kind="bar",
        x="result",
        y="occurences",
        hue="team",
        palette="dark",
        alpha=0.75,
    )
    plt.show()


def sessionLength():
    plotData = {
        "length": [],
        "occurences": [],
    }


# scoreOccurence()
df = pd.DataFrame(eloOverSeason())
sns.set_theme(style="whitegrid")
sns.lineplot(data=df, x="sessionNumber", y="elo", palette="pastel", alpha=0.75)

plt.show()
