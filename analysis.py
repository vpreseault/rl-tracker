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

    for session in data["s14"]["doubles"]["sessions"]:
        for elo in session["estimatedMmr"]:
            plotData["elo"].append(elo)
            numberOfSessions += 1
    plotData["sessionNumber"] = list(range(1, numberOfSessions + 1))

    return plotData


def resultsAfter3Games():
    plotData = {"results": ["3L", "2L W1", "1L 2W", "3W"], "occurences": [0, 0, 0, 0]}
    for session in data["s14"]["doubles"]["sessions"]:
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
    for session in data["s14"]["doubles"]["sessions"]:
        if session["chat"]:
            plotData["occurences"][0] += 1
        else:
            plotData["occurences"][1] += 1
    return plotData


df = pd.DataFrame(eloOverSeason())
sns.set_theme(style="whitegrid")
sns.lineplot(data=df, x="sessionNumber", y="elo", palette="pastel", alpha=0.75)

plt.show()
