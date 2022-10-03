from random import sample
import discord
import players
from config import config

## Teams
# Name, user_id, boolean(0 : bot, 1 : player, form)
f_teams = config["dataPath"] + "teams.csv"

async def get(id):
    print("called")
    # Find team which owned by called player
    with open(f_teams, "r") as tfile:
        teamfile = tfile.readlines()

        for line in teamfile:
            try:
                if id == str(line.split(",")[1]):
                    return line
            except:
                continue

async def getAll(id):
    user_id = str(id)
    t_info = await get(user_id)
    default_color = 0xffff00

    if t_info is None:
        return discord.Embed(title="No team found!", description="", color=default_color)
    elif t_info == "Error":
        return discord.Embed(title="Error", description="An error occurred during the request to get the teams.", color=default_color)
    else:
        p_info = await players.get(user_id)
        team_name = t_info.split(",")[0]

        i = 0
        default_color = 0x00ff00

        embedteam = discord.Embed(
            title=team_name, description="Below your squad", color=default_color)

        embeddescription = ""

        while i <= 5:
            if i == 0:
                i += 1

            name = p_info[i].displayName
            ovr = p_info[i].ovr
            pos = p_info[i].pos.upper()
            nat = p_info[i].nat
            #nft = p_info[i].split(",")[5]
            rarity = p_info[i].rarity
            rarity_flag = "⚫"

            if rarity == "common":
                rarity_flag = "⚪"
            elif rarity == "uncommon":
                rarity_flag = "🟢"
            elif rarity == "rare":
                rarity_flag = "🔵"
            elif rarity == "legend":
                rarity_flag = "🟣"

            if len(pos) == 3:
                embeddescription = embeddescription + ":flag_" + nat + ":`" + pos + " " + str(ovr) + "`" + rarity_flag + " *" + name + "*\n"
            else:
                embeddescription = embeddescription + ":flag_" + nat + ":`" + pos + "  " + str(ovr) + "`" + rarity_flag + " *" + name + "*\n"
            i += 1

        man_name = p_info[0].displayName
        embedmanager = "*" + man_name + "*"
        embedteam.add_field(name="Players", value=embeddescription)
        embedteam.add_field(name="Coach", value=embedmanager, inline=False)

        return embedteam

async def find(id):
    with open(f_teams, "r") as tfile:
        teamfile = tfile.readlines()
        teamlist = []
        genopponent = sample(range(0, len(teamfile)), 5)
        selected = 0

        for x in genopponent:
            if selected < 3:
                try:
                    teamid = str(teamfile[x].split(",")[1])
                    if id == teamid:
                        continue
                    else:
                        username = str(teamfile[x].split(",")[4])
                    name = str(teamfile[x].split(",")[0])
                    teamlist.append(name + "," + teamid + "," + username)
                    selected += 1
                except:
                    continue

        default_color = 0x00ff00

        embedteam = discord.Embed(
            title="Match Settings", description="Choose your opponent or play an event", color=default_color)

        embedopponents = "`" + teamlist[0].split(",")[0] + "` *" + teamlist[0].split(",")[2] + "*\n"
        embedopponents = embedopponents + "`" + teamlist[1].split(",")[0] + "` *" + teamlist[1].split(",")[2] + "*\n"
        embedteam.add_field(name="Opponents", value=embedopponents)

        return embedteam, teamlist

