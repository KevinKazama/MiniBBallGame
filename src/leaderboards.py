import discord
import events
from config import config

async def get(name_event, teamname):
    i = name_event

    f_goals = config["dataPath"] + "goals.csv"
    f_points = config["dataPath"] + "points.csv"
    leaderboard = "byPlayer"
    reward = 0
    nbgoal = 0

    if "event_" in i:
        event = await events.getbyCode(i)
        leaderboard = event[0].leaderboard
        reward = event[0].reward
        f_goals = config["dataPath"] + "goals_" + i + ".csv"

    print(i)
    if i == "points":
        f_goals = f_points
        leaderboard = "byTeam"

    with open(f_goals, "r") as tgoals:
        goalfile = tgoals.readlines()
        goalfile.sort(reverse=True, key=lambda x: int(x.split(",")[0]))
        embedscore = ""
        indice = 1
        embeduser = "\u200b"

        for line in goalfile:
            number = line.split(",")[0]
            team = line.split(",")[1]
            if int(reward) > 0:
                nbgoal += int(number)
            if indice <= 10:
                number = line.split(",")[0]
                team = line.split(",")[1]
                if leaderboard == "byPlayer":
                    name = line.split(",")[2]
                    embedscore = embedscore + "**"+ str(number) + "** : " + name + " (*" + team + "*)\n"
                else:
                    embedscore = embedscore + team + " - **"+ str(number) + "pts**\n"
                indice += 1
            if teamname == team:
                if embeduser == "\u200b":
                    if leaderboard == "byPlayer":
                        name = line.split(",")[2]
                        embeduser = "**"+ str(number) + "** : " + name + " (*" + team + "*)\n"
                    if leaderboard == "byTeam":
                        embeduser = team + " - **"+ str(number) + "pts**\n"


        if embedscore == "":
            embedscore = "\u200b"

        if embeduser != "\u200b":
            embedscore = embedscore + "--------\n" + embeduser

        default_color = 0x00ff00

        if "event_" in i:
            name = i.split("_")[1].upper()
            embedlead = discord.Embed(
                title="Leaderboards", description="Top 10 for **"+name+"** event", color=default_color)
        else:
            embedlead = discord.Embed(
                title="Leaderboards", description="Top 10", color=default_color)

        embedlead.add_field(name="Ranking", value=embedscore)
        if int(reward) > 0:
            embedlead.add_field(name="Road to "+str(reward)+" goals !", value=str(nbgoal)+"/"+str(reward), inline=False)

        return embedlead
