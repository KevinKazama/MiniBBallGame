import asyncio
import discord
from discord.ui import View, Button
from discord.ext import commands
from random import randint
import events
import leaderboards
import matchengine
import nfts
import players
import teams
import cooldown
import nations
from config import config
import discordUtils

### Prerequisites
# Discord2 Python library (py-cord)
# asyncio library
# names library to generate random names

### Files
## Players (DisplayName, OVR, Position, Owner, nationality, nft, rarity)
f_players = config["dataPath"] + "players.csv"
## Teams
# Name, user_id, boolean(0 : bot, 1 : player, form)
f_teams = config["dataPath"] + "teams.csv"
## Goal scorers (number, name, team)
f_goals = config["dataPath"] + "goals.csv"
## Event (name, desc, status)
f_events = config["dataPath"] + "events.csv"

#load_dotenv(dotenv_path="config")
intents = discord.Intents.all()

### Set prefix
bot = discord.Bot()

### Discord configurations ###
adminid = config["adminId"]
gamechan = config["gameChan"]

async def callmatch(team1, team2, event):

    match = await matchengine.play(str(team1), str(team2), event)
    view = View()
    color = 0x00ff00
    embedmenu = discord.Embed(
        title='Discord Football Game', color=color)

    return view, embedmenu, match


########################################################################################################
## START OF PROCESS ##
########################################################################################################

#### BOT IS READY ####
@bot.event
async def on_ready():
    print("Bot Ready")

#### CREATE TEAM ####
@bot.command(name='create', description='The first step to enter into the game...')
async def create(ctx):
    # Usage : !create Team_Name
    if str(ctx.channel.id) in gamechan:
        with open(f_teams, "r+") as tfile:
            user = ctx.interaction.user
            user_id = str(user.id)
            if user.id > 1000000:
                username = user.name if user.nick is None else user.nick
                teamname = "FC "+ username
            else:
                username = "BOT"
            team_id = user_id
            if user_id in tfile.read():
                if str(user_id) in adminid:
                    team_id = str(randint(1, 999999))
                    teamname = "Team"+str(randint(1,1000))
                    tfile.write(teamname + "," + team_id + ",no,3,BOT,\n")
                    await players.create(team_id, username)
                    await ctx.respond(teamname + " created !", ephemeral=True)
                else:
                    await ctx.respond("Sorry, you already have a team !", ephemeral=True)
            else:
                tfile.write(teamname + "," + team_id + ",yes,3,"+username+"\n")
                await players.create(team_id, username)
                await ctx.respond("Team " + teamname + " created !", ephemeral=True)

@bot.command(name='view')
async def change(ctx, user: discord.User):
    if str(ctx.channel.id) in gamechan:
        embedteam = await teams.getAll(str(user.id))
        await ctx.respond(embed=embedteam, ephemeral=False)


@bot.command(name='match', description="Start a match !", hidden=True)
async def match(ctx, user1: discord.User, user2: discord.User):
    user_id = str(ctx.interaction.user.id)
    if (str(ctx.channel.id) in gamechan) and (user_id in adminid):
        team1 = str(user1.id)
        team2 = str(user2.id)
        event = "match"
        view, embedmenu, match = await callmatch(team1, team2, event)
        showmenu = await ctx.respond("\u200b", view=view, embed=embedmenu, ephemeral=False)

        for x in match:
            await showmenu.edit_original_message(view=view, embed=x)
            await asyncio.sleep(1)
    else:
        await ctx.respond("You have no right to use this command !", ephemeral=True)


@bot.command(name='intmatch', description="Start a match !", hidden=True)
async def intmatch(ctx, team1:str, team2:str):
    user_id = str(ctx.interaction.user.id)
    if (str(ctx.channel.id) in gamechan) and (user_id in adminid):
        event = "international"

        view, embedmenu, match = await callmatch(team1, team2, event)
        showmenu = await ctx.respond("\u200b", view=view, embed=embedmenu, ephemeral=False)

        for x in match:
            await showmenu.edit_original_message(view=view, embed=x)
            await asyncio.sleep(1)
    else:
        await ctx.respond("You have no right to use this command !", ephemeral=True)


@bot.command(name='versus', description="Start a match !")
async def match(ctx, user2: discord.User):
    if str(ctx.channel.id) in gamechan:
        user1 = ctx.interaction.user
        team1 = str(user1.id)
        team2 = str(user2.id)
        event = "versus"

        view, embedmenu, match = await callmatch(team1, team2, event)
        showmenu = await ctx.respond("\u200b", view=view, embed=embedmenu, ephemeral=False)

        for x in match:
            await showmenu.edit_original_message(view=view, embed=x)
            await asyncio.sleep(1)


#### Menu display
@bot.command(name='game', description='Access to the menu, build your team and compete...')
async def game(ctx):
    if str(ctx.channel.id) in gamechan:
        user_id = str(ctx.interaction.user.id)
        user_name = str(ctx.interaction.user)
        default_color = 0x00ff00
        embedmenu = discord.Embed(
            title='Ballerz Discord Game', color=default_color)
        description = "\nYour players are currently in the training field...\n" \
                    "If I were you, I'll have a look at what's going on: *Missed passes, uncontrolled shots*...\n\n" \
                    "It seems you have a lot to do with them. But it's not my business, you're the boss here! 😉\n\n" \
                    "Let me remind you what the buttons below are for:\n" \
                    "**👥 Manage my Team** : Access to your line-up\n" \
                    "╠═ **🎉 My Ballerz**: You have a Ballerz player in your wallet? Put him in your team!\n" \
                    "╚═ **👨 Scout**: Find a non-NFT player and recruit him if he is good enough :fire:.\n" \
                    "**⚽ Play**: Send your players on the field against another team.\n" \
                    "**🏆 Leaderboard**: Is there a world where your forward is the best scorer of the game?"
        #"**National Team** : Bring your country into the top of the world !"
        embedmenu.add_field(name="Hello coach "+user_name.split("#")[0]+ " !", value=description, inline=True)
        embedmenu.set_thumbnail(url="")

        button_play = Button(label="Play", style=discord.ButtonStyle.blurple, custom_id="play", emoji="🏀")
        button_scout = Button(label="Scout", style=discord.ButtonStyle.green, custom_id="scout", emoji="👨")
        button_nfts = Button(label="My Ballerz", style=discord.ButtonStyle.green, custom_id="nfts", emoji="🎉")
        button_nt = Button(label="National Team", style=discord.ButtonStyle.green,
                           row=2, custom_id="nt", emoji="🎌")
        button_manage_team = Button(label="Manage my Team", style=discord.ButtonStyle.green, custom_id="manage_team", emoji="👥")
        button_recruit = Button(label="Recruit", style=discord.ButtonStyle.green, custom_id="recruit", emoji="✅")
        button_replace = Button(label="Replace", style=discord.ButtonStyle.green, custom_id="replace", emoji="✅")
        button_return = Button(label="Return", style=discord.ButtonStyle.grey, custom_id="return", emoji="⬅", row=3)
        button_stats = Button(label="Stats", style=discord.ButtonStyle.green, custom_id="stats", emoji="🔢", row=3)
        button_finishmatch = Button(label="Skip", style=discord.ButtonStyle.green, custom_id="finishmatch")
        button_leaderboard = Button(label="Leaderboard", style=discord.ButtonStyle.green, row=1, custom_id="leaderboard",
                                    emoji="🏆")
        #button_events = Button(label="Events", style=discord.ButtonStyle.green, row=1, custom_id="eventName", emoji="⭐")

        view_def = View()
        view_def.add_item(button_manage_team)
        #view_def.add_item(button_events)
        view_def.add_item(button_leaderboard)

        view_match = View()
        view_match.add_item(button_finishmatch)
        view_match.add_item(button_return)

        skip = 0

        async def button_play_callback(interaction):
            if str(interaction.user) == user_name:
                embed_opponents, list_teams = await teams.find(user_id)
                list_events = await events.get("vs")

                view_opponents = View()

                i = 1

                if list_events[0] is not None:
                    button_ev1 = None
                    button_ev2 = None
                    button_ev3 = None
                    button_ev4 = None
                    button_ev5 = None

                    for event in list_events:
                        code = event.code
                        teamName = event.name
                        desc = event.desc
                        status = event.status
                        kind = event.kind
                        opponent = event.opponent


                id_random = str(list_teams[2].split(",")[1])
                button_random = Button(label="vs Random", style=discord.ButtonStyle.grey, custom_id=id_random,
                                       emoji="⚽")
                view_opponents.add_item(button_random)

                i = 1
                for x in list_teams:
                    teamName = x.split(",")[0]
                    teamId = x.split(",")[1]
                    print(teamId)
                    if i == 1:
                        button_vs1 = Button(label=teamName, style=discord.ButtonStyle.green, custom_id=str(teamId))
                        view_opponents.add_item(button_vs1)
                    elif i == 2:
                        button_vs2 = Button(label=teamName, style=discord.ButtonStyle.green, custom_id=str(teamId))
                        view_opponents.add_item(button_vs2)
                    i += 1

                view_opponents.add_item(button_return)

                await showmenu.edit_original_message(view=view_opponents, embed=embed_opponents)
                await interaction.response.defer()

                async def button_vs_callback(interaction):
                    if str(interaction.user) == user_name:
                        global skip
                        skip = 0

                        cooldown.add_cd_match(user_name)
                        view_match = View()
                        view_match.add_item(button_finishmatch)
                        view_match.add_item(button_return)

                        opponent = interaction.data['custom_id']
                        print(opponent)
                        if "event_" in opponent:
                            eventName = opponent.split(",")[0]
                            opponent = opponent.split(",")[1]
                        else:
                            eventName = "no"

                        print(opponent)
                        list_embed_match, playershome, playersaway = await matchengine.play(user_id, opponent, eventName)
                        i = 1

                        async def button_stats_callback(interaction):
                            if str(interaction.user) == user_name:
                                view_match = View()
                                view_match.add_item(button_return)
                                nb = 1
                                embeddesr = "`Poi Reb Ass`\n"
                                while nb < 6:
                                    if playershome[nb].points > 9:
                                        embeddesr = embeddesr + "`" + str(playershome[nb].points) + "  " + str(
                                            playershome[nb].rebounds) + "   " + str(
                                            playershome[nb].assists) + "  ` **" + playershome[nb].displayName + "**\n"
                                    else:
                                        embeddesr = embeddesr + "`" + str(playershome[nb].points) + "   " + str(playershome[nb].rebounds) + "   " + str(playershome[nb].assists) + "  ` **"+playershome[nb].displayName + "**\n"
                                    nb += 1
                                list_embed_match[-1].add_field(name="Stats", value=embeddesr, inline=False)
                                await showmenu.edit_original_message(view=view_match, embed=list_embed_match[-1])
                                await interaction.response.defer()

                        button_stats.callback = button_stats_callback

                        async def button_finishmatch_callback(interaction):
                            global skip

                            if str(interaction.user) == user_name:
                                skip = 1
                                view_finishmatch = View()
                                view_finishmatch.add_item(button_stats)
                                view_finishmatch.add_item(button_return)
                                await showmenu.edit_original_message(view=view_finishmatch, embed=list_embed_match[-1])
                                await interaction.response.defer()

                        for x in list_embed_match:
                            if i == len(list_embed_match) - 1:
                                skip == 1
                            i += 1

                            button_finishmatch.callback = button_finishmatch_callback

                            if skip == 1:
                                break

                            await showmenu.edit_original_message(view=view_match, embed=x)
                            await asyncio.sleep(1)

                            try:
                                await interaction.response.defer()
                            except discord.InteractionResponded:
                                continue



                button_random.callback = button_vs_callback
                button_vs1.callback = button_vs_callback
                button_vs2.callback = button_vs_callback
                if button_ev1:
                    button_ev1.callback = button_vs_callback
                if button_ev2:
                    button_ev2.callback = button_vs_callback
                if button_ev3:
                    button_ev3.callback = button_vs_callback
                if button_ev4:
                    button_ev4.callback = button_vs_callback
                if button_ev5:
                    button_ev5.callback = button_vs_callback

        async def button_return_callback(interaction):
            if str(interaction.user) == user_name:
                embed_team = await teams.getAll(user_id)

                check_cooldown = cooldown.check(user_name)

                view = View()
                view.add_item(button_manage_team)
                #view.add_item(button_events)
                view.add_item(button_leaderboard)
                #view.add_item(button_nt)

                description = ""

                if "scout" in check_cooldown.keys():
                    end_cooldown = check_cooldown["scout"]
                    description = description + "Scout until " + discordUtils.formatDateTimeForDiscord(end_cooldown) + " \n"


                if "match" in check_cooldown.keys():
                    end_cooldown = check_cooldown["match"]
                    description = description + "Match until " + discordUtils.formatDateTimeForDiscord(end_cooldown)

                else:
                    view.add_item(button_play)

                if description != "":
                    embed_team.add_field(name="Cooldown", value=description)

                await showmenu.edit_original_message(view=view, embed=embed_team)
                await interaction.response.defer()

        async def button_manage_team_callback(interaction):
            if str(interaction.user) == user_name:
                embed_team = await teams.getAll(user_id)

                check_cooldown = cooldown.check(user_name)

                view = View()
                view.add_item(button_return)
                view.add_item(button_nfts)

                description = ""
                if "scout" in check_cooldown.keys():
                    end_cooldown = check_cooldown["scout"]
                    description = description + "Scout until " + discordUtils.formatDateTimeForDiscord(end_cooldown) + " \n"
                else:
                    view.add_item(button_scout)

                if "match" in check_cooldown.keys():
                    end_cooldown = check_cooldown["match"]
                    description = description + "Match until " + discordUtils.formatDateTimeForDiscord(end_cooldown)

                else:
                    view.add_item(button_play)

                if description != "":
                    embed_team.add_field(name="Cooldown", value=description)

                await showmenu.edit_original_message(view=view, embed=embed_team)
                await interaction.response.defer()

        async def button_nfts_callback(interaction):
            if str(interaction.user) == user_name:
                global indice
                indice = 0

                await interaction.response.defer()

                list_players = await nfts.get(user_id, indice)

                async def nftembed(playerslist, indice):
                    default_color = 0xffff00
                    embednfts = discord.Embed(
                        title="Your NFTS", description="Below your squad", color=default_color)
                    description = ""
                    buttons = []
                    b1 = None
                    b2 = None
                    b3 = None
                    b4 = None
                    b5 = None
                    i = 0
                    if len(playerslist) > 0:
                        indice = indice % len(playerslist)
                        for x in playerslist[indice]:
                            nation = x.split(",")[0]
                            positions = x.split(",")[1]
                            ovr = x.split(",")[2]
                            displayName = x.split(",")[3]
                            rarity = x.split(",")[4]

                            if rarity == "common":
                                rarity_flag = "⚪"
                            elif rarity == "uncommon":
                                rarity_flag = "🟢"
                            elif rarity == "rare":
                                rarity_flag = "🔵"
                            elif rarity == "legend":
                                rarity_flag = "🟣"

                            if len(positions) == 3:
                                description = description + ":flag_" + nation + ":`" + positions + " " + str(
                                    ovr) + "`" + rarity_flag + " *" + displayName + "*\n"
                            else:
                                description = description + ":flag_" + nation + ":`" + positions + "  " + str(
                                    ovr) + "`" + rarity_flag + " *" + displayName + "*\n"

                            if i == 0:
                                b1 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                                buttons.append(b1)
                            elif i == 1:
                                b2 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                                buttons.append(b2)
                            elif i == 2:
                                b3 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                                buttons.append(b3)
                            elif i == 3:
                                b4 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                                buttons.append(b4)
                            elif i == 4:
                                b5 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                                buttons.append(b5)
                            i += 1
                    else:
                        description = "It seems that you don't have NFTs.\nDon't forget to link your Discord account " \
                                      "to your Dapper Wallet. "

                    embednfts.add_field(name="Players", value=description)

                    viewnfts = View()
                    if len(playerslist) > 0:
                        viewnfts.add_item(button_previous)
                        viewnfts.add_item(button_next)
                    viewnfts.add_item(button_return)

                    async def button_scoutnft_callback(interaction):
                        if str(interaction.user) == user_name:
                            viewscout = View()
                            viewscout.add_item(button_recruit)
                            viewscout.add_item(button_return)

                            select = int(interaction.data['custom_id'].split(" ")[1])

                            player = playerslist[indice][select]
                            nat = player.split(",")[0]
                            pos = player.split(",")[1]
                            ovr = player.split(",")[2]
                            name = player.split(",")[3]
                            rarity = player.split(",")[4]

                            alreadyinTeam = await players.check(user_id, name)

                            if alreadyinTeam == True:

                                default_color = 0xffff00
                                embedscout = discord.Embed(
                                    title="Error", description="This player is already in your team", color=default_color)

                                view = View()
                                view.add_item(button_return)
                                view.add_item(button_nfts)

                                await showmenu.edit_original_message(view=view, embed=embedscout)
                                await interaction.response.defer()

                            else:
                                embedscout = await nfts.scout(user_id, name, ovr, pos, nat, rarity)

                                await showmenu.edit_original_message(view=viewscout, embed=embedscout)
                                await interaction.response.defer()

                    if b1:
                        b1.callback = button_scoutnft_callback
                    if b2:
                        b2.callback = button_scoutnft_callback
                    if b3:
                        b3.callback = button_scoutnft_callback
                    if b4:
                        b4.callback = button_scoutnft_callback
                    if b5:
                        b5.callback = button_scoutnft_callback

                    for x in buttons:
                        viewnfts.add_item(x)

                    return embednfts, viewnfts

                async def button_move_callback(interaction):
                    global indice
                    if str(interaction.user) == user_name:
                        page = interaction.data['custom_id']
                        if page == "next":
                            indice += 1
                        elif page == "prev":
                            indice -= 1

                        embednfts, viewnfts = await nftembed(list_players, indice)


                        await showmenu.edit_original_message(view=viewnfts, embed=embednfts)
                        await interaction.response.defer()

                button_previous = Button(style=discord.ButtonStyle.green, custom_id="prev", emoji="◀")
                button_next = Button(style=discord.ButtonStyle.green, custom_id="next", emoji="▶")
                button_next.callback = button_move_callback
                button_previous.callback = button_move_callback

                embednfts, viewnfts = await nftembed(list_players, indice)

                await showmenu.edit_original_message(view=viewnfts, embed=embednfts)
                #await interaction.response.defer()

        async def button_nt_callback(interaction):
            if str(interaction.user) == user_name:

                teaminfo = await nations.check(user_id)

                if teaminfo is None:
                    embedteam = discord.Embed(
                        title="National Team",
                        description="You have no team to manage",
                        color=default_color)
                else:
                    embedteam = await nations.getAll(teaminfo.displayName)

                async def button_ntplayers_callback(interaction):
                    if str(interaction.user) == user_name:
                        global indice
                        indice = 0

                        playerslist = await nations.getList(teaminfo.displayName)

                        async def nftembed(playerslist, indice):
                            default_color = 0xffff00
                            embednfts = discord.Embed(
                                title="Your NFTS", description="Below your squad", color=default_color)
                            description = ""
                            buttons = []
                            b1 = None
                            b2 = None
                            b3 = None
                            b4 = None
                            b5 = None
                            i = 0

                            indice = indice % len(playerslist)
                            for x in playerslist[indice]:
                                displayName = x.split(",")[0]
                                ovr = x.split(",")[1]
                                positions = x.split(",")[2]
                                nation = x.split(",")[3]
                                prefix_nat = x.split(",")[4]
                                rarity = x.split(",")[6]

                                rarity_flag = "⚪"

                                if rarity == "common":
                                    rarity_flag = "⚪"
                                elif rarity == "uncommon":
                                    rarity_flag = "🟢"
                                elif rarity == "rare":
                                    rarity_flag = "🔵"
                                elif rarity == "legend":
                                    rarity_flag = "🟣"

                                if len(positions) == 3:
                                    description = description + ":flag_" + prefix_nat + ":`" + positions + " " + str(
                                        ovr) + "`" + rarity_flag + " *" + displayName + "*\n"
                                else:
                                    description = description + ":flag_" + prefix_nat + ":`" + positions + "  " + str(
                                        ovr) + "`" + rarity_flag + " *" + displayName + "*\n"

                                if i == 0:
                                    b1 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1,
                                                custom_id="Player " + str(i))
                                    buttons.append(b1)
                                elif i == 1:
                                    b2 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1,
                                                custom_id="Player " + str(i))
                                    buttons.append(b2)
                                elif i == 2:
                                    b3 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1,
                                                custom_id="Player " + str(i))
                                    buttons.append(b3)
                                elif i == 3:
                                    b4 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1,
                                                custom_id="Player " + str(i))
                                    buttons.append(b4)
                                elif i == 4:
                                    b5 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1,
                                                custom_id="Player " + str(i))
                                    buttons.append(b5)
                                i += 1

                            embednfts.add_field(name="Players", value=description)

                            viewnfts = View()
                            viewnfts.add_item(button_previous)
                            viewnfts.add_item(button_next)
                            viewnfts.add_item(button_return)

                            async def button_search_callback(interaction):
                                if str(interaction.user) == user_name:
                                    viewnt = View()
                                    viewnt.add_item(button_replace)
                                    viewnt.add_item(button_return)

                                    select = int(interaction.data['custom_id'].split(" ")[1])
                                    player = playerslist[indice][select]
                                    print(player)
                                    name = player.split(",")[0]
                                    ovr = player.split(",")[1]
                                    pos = player.split(",")[2]
                                    nation = player.split(",")[3]
                                    prefix_nat = player.split(",")[4]
                                    rarity = player.split(",")[6]


                                    alreadyinTeam = await nations.alreadyinTeam(nation, name)

                                    if alreadyinTeam == True:

                                        default_color = 0xffff00
                                        embedscout = discord.Embed(
                                            title="Error", description="This player is already in your team",
                                            color=default_color)

                                        view = View()
                                        view.add_item(button_return)
                                        view.add_item(button_nt)

                                        await showmenu.edit_original_message(view=view, embed=embedscout)
                                        await interaction.response.defer()

                                    else:

                                        embedscout = await nations.search(nation, name, ovr, pos, prefix_nat, rarity)

                                        await showmenu.edit_original_message(view=viewnt, embed=embedscout)
                                        await interaction.response.defer()

                            if b1:
                                b1.callback = button_search_callback
                            if b2:
                                b2.callback = button_search_callback
                            if b3:
                                b3.callback = button_search_callback
                            if b4:
                                b4.callback = button_search_callback
                            if b5:
                                b5.callback = button_search_callback

                            for x in buttons:
                                viewnfts.add_item(x)

                            return embednfts, viewnfts



                        async def button_move_callback(interaction):

                            global indice
                            if str(interaction.user) == user_name:
                                page = interaction.data['custom_id']
                                print(indice)
                                if page == "next":
                                    indice += 1
                                elif page == "prev":
                                    indice -= 1

                                embednfts, viewnfts = await nftembed(playerslist, indice)

                                await showmenu.edit_original_message(view=viewnfts, embed=embednfts)
                                await interaction.response.defer()

                        ### Generate embed

                        button_previous = Button(style=discord.ButtonStyle.blurple, custom_id="prev", emoji="◀")
                        button_next = Button(style=discord.ButtonStyle.blurple, custom_id="next", emoji="▶")
                        button_next.callback = button_move_callback
                        button_previous.callback = button_move_callback

                        embednt, viewnt = await nftembed(playerslist, indice)

                        await showmenu.edit_original_message(view=viewnt, embed=embednt)
                        await interaction.response.defer()



                button_ntplayers = Button(label="Players list", style=discord.ButtonStyle.green, custom_id="ntplayers")
                button_ntplayers.callback = button_ntplayers_callback

                viewnt = View()
                viewnt.add_item(button_return)
                viewnt.add_item(button_ntplayers)

                await showmenu.edit_original_message(view=viewnt, embed=embedteam)
                await interaction.response.defer()


        async def button_scout_callback(interaction):
            if str(interaction.user) == user_name:
                cooldown.add_cd_scout(user_name)
                viewscout = View()
                viewscout.add_item(button_recruit)
                viewscout.add_item(button_return)
                embedplayer = await players.scout(user_id)
                await showmenu.edit_original_message(view=viewscout, embed=embedplayer)
                await interaction.response.defer()

        async def button_leaderboard_callback(interaction):
            if str(interaction.user) == user_name:

                username = interaction.user.name if interaction.user.nick is None else interaction.user.nick
                teamname = "FC "+username
                viewlead = View()
                viewlead.add_item(button_return)

                embedlead = await leaderboards.get("none", teamname)
                eventlist = await events.get("all")
                i = 1

                button_global = Button(label="Scorers", style=discord.ButtonStyle.blurple,
                                        row=1, custom_id="goals")
                viewlead.add_item(button_global)

                button_points = Button(label="Teams", style=discord.ButtonStyle.blurple,
                                                        row=1, custom_id="points")
                viewlead.add_item(button_points)

                if eventlist[0] != "":
                    button_ev1 = None
                    button_ev2 = None
                    button_ev3 = None
                    button_ev4 = None
                    button_ev5 = None

                    for event in eventlist:
                        code = event.code
                        name = event.name
                        desc = event.desc
                        status = event.status
                        kind = event.kind
                        opponent = event.opponent

                        #if i == 1:
                        #    button_ev1 = Button(label=name, style=discord.ButtonStyle.blurple,
                        #                            row=2, custom_id=code+","+opponent)
                        #    viewlead.add_item(button_ev1)
                        #elif i == 2:
                        #    button_ev2 = Button(label=name, style=discord.ButtonStyle.blurple,
                        #                            row=2, custom_id=code+","+opponent)
                        #    viewlead.add_item(button_ev2)
                        #elif i == 3:
                        #    button_ev3 = Button(label=name, style=discord.ButtonStyle.blurple,
                        #                            row=2, custom_id=code+","+opponent)
                        #    viewlead.add_item(button_ev3)
                        #elif i == 4:
                        #    button_ev4 = Button(label=name, style=discord.ButtonStyle.blurple,
                        #                            row=2, custom_id=code+","+opponent)
                        #    viewlead.add_item(button_ev4)
                        #elif i == 5:
                        #    button_ev5 = Button(label=name, style=discord.ButtonStyle.blurple,
                        #                            row=2, custom_id=code+","+opponent)
                        #    viewlead.add_item(button_ev5)
                        #i += 1

                async def button_leads_callback(interaction):
                    event = interaction.data['custom_id'].split(",")[0]

                    embedlead = await leaderboards.get(event, teamname)

                    await showmenu.edit_original_message(view=viewlead, embed=embedlead)
                    await interaction.response.defer()


                button_global.callback = button_leads_callback
                button_points.callback = button_leads_callback
                if button_ev1:
                    button_ev1.callback = button_leads_callback
                if button_ev2:
                    button_ev2.callback = button_leads_callback
                if button_ev3:
                    button_ev3.callback = button_leads_callback
                if button_ev4:
                    button_ev4.callback = button_leads_callback
                if button_ev5:
                    button_ev5.callback = button_leads_callback

                await showmenu.edit_original_message(view=viewlead, embed=embedlead)
                await interaction.response.defer()

        async def button_events_callback(interaction):
            if str(interaction.user) == user_name:
                eventlist = await events.get("all")

                view = View()
                view.add_item(button_return)
                view.add_item(button_leaderboard)

                default_color = 0x00ff00
                embedevent = discord.Embed(
                    title="Events", description="Below the list of current eventName", color=default_color)

                for event in eventlist:
                    code = event.code
                    name = event.name
                    desc = event.desc
                    status = event.status
                    kind = event.kind

                    embedevent.add_field(name=name, value=desc)

                await showmenu.edit_original_message(view=view, embed=embedevent)
                await interaction.response.defer()

        async def button_recruit_callback(interaction):
            if str(interaction.user) == user_name:
                playerscheck = interaction.message.embeds[0].fields
                playersinfos = playerscheck[0].value.split(" ")
                nat = playersinfos[0].split("`")[0].split("_")[1].replace(":", "")
                num = playersinfos[0].split("`")[1]

                pos = playersinfos[2]
                ovr = playersinfos[3].replace("`", "")
                name = playersinfos[5] + " " + playersinfos[6]
                if len(playersinfos) > 7:
                    name = name + " " + playersinfos[7]

                name = name.replace("*", "")
                await players.recruit(user_id, num, name, ovr, pos, nat)
                embedteam = await teams.getAll(user_id)

                view = View()
                view.add_item(button_return)
                view.add_item(button_scout)
                view.add_item(button_nfts)

                await showmenu.edit_original_message(view=view, embed=embedteam)
                await interaction.response.defer()

        async def button_replace_callback(interaction):
            if str(interaction.user) == user_name:
                playerscheck = interaction.message.embeds[0].fields
                playersinfos = playerscheck[0].value.split(" ")
                nat = playersinfos[0].split("`")[0].split("_")[1].replace(":", "")
                num = playersinfos[0].split("`")[1]
                pos = playersinfos[2]
                ovr = playersinfos[3].replace("`", "")
                name = playersinfos[5] + " " + playersinfos[6]
                if len(playersinfos) > 7:
                    name = name + " " + playersinfos[7]

                name = name.replace("*", "")
                await nations.replace(num, name, ovr, pos, nat)
                embedteam = await nations.getAll(nat)

                view = View()
                view.add_item(button_return)
                view.add_item(button_nt)

                await showmenu.edit_original_message(view=view, embed=embedteam)
                await interaction.response.defer()

        button_play.callback = button_play_callback
        #button_events.callback = button_events_callback
        button_leaderboard.callback = button_leaderboard_callback
        #button_team.callback = button_team_callback
        button_manage_team.callback = button_manage_team_callback
        button_scout.callback = button_scout_callback
        button_recruit.callback = button_recruit_callback
        button_replace.callback = button_replace_callback
        button_return.callback = button_return_callback
        button_nfts.callback = button_nfts_callback
        button_nt.callback = button_nt_callback

        check_cooldown = cooldown.check(user_name)

        view = view_def
        if "scout" in check_cooldown.keys():
            end_cooldown = check_cooldown["scout"]
            value = "Scout until " + discordUtils.formatDateTimeForDiscord(end_cooldown)
            embedmenu.add_field(name="Cooldown", value=value)

        if "match" in check_cooldown.keys():
            end_cooldown = check_cooldown["match"]
            value = "Match until " + discordUtils.formatDateTimeForDiscord(end_cooldown)
            embedmenu.add_field(name="Cooldown", value=value)
        else:
            view.add_item(button_play)
        embedmenu.set_image(url="https://d13e14gtps4iwl.cloudfront.net/discord/logo.jpg")

        showmenu = await ctx.respond("\u200b", view=view, embed=embedmenu, ephemeral=True)

bot.run(config["botToken"])


