import random
import discord
from random import randint
import events
import teams
import players
import commentaries
import nations
from config import config

f_goals = config["dataPath"] + "goals.csv"
f_points = config["dataPath"] + "points.csv"

class Teams:
    def __init__(self, home, away):
        self.home = home
        self.away = away

class Score:
    def __init__(self, home, away):
        self.home = home
        self.away = away

class Event:
    def __init__(self, kind, player, team, quarter, minute):
        self.kind = kind
        self.player = player
        self.team = team
        self.quarter = quarter
        self.minute = minute

class MatchEvent:
    def __init__(self, teams: Teams, score: Score, event, commentary, quarter, minutes, note):
        self.teams = teams
        self.score = score
        self.event = event
        self.commentary = commentary
        self.quarter = quarter
        self.minutes = minutes
        self.note = note

async def simulate(id, vs, event):
    # Find player's team information
    eventinfo = await events.getbyCode(event)
    leads = "byPlayer"

    if len(eventinfo) > 0:
        leads = eventinfo[0].leaderboard

    if event == "international":
        t_info = await nations.get(id)
        playershome = await players.getnation(id)
        if len(playershome) == 5:
            playershome.insert(0, "Manager")

    else:
        t_info = await teams.get(id)
        playershome = await players.get(id)

    def player_form(teamform):

        i = randint(1, 100)
        dict_form = {
            0: -5,
            1: -3,
            2: -1,
            3: 1,
            4: 3,
            5: 5
        }
        try:
            playerform = int(teamform)
        except:
            playerform = 3

        if i < 30:
            playerform -= 1
        if i > 70:
            playerform += 1
        if playerform < 0:
            playerform = 0
        elif playerform > 5:
            playerform = 5

        playerbonus = dict_form[playerform]

        return playerbonus

    if event == "international":
        t_vs_info = await nations.get(vs)
        playersaway = await players.getnation(vs)
        if len(playersaway) == 5:
            playersaway.insert(0, "Manager")

    else:
        t_vs_info = await teams.get(vs)
        playersaway = await players.get(vs)

    team_name_away = t_vs_info.split(",")[0]
    try:
        team_form_away = t_vs_info.split(",")[3]
    except:
        team_form_away = 3

    away_man = playersaway[0]
    away_ovr_list = []
    for x in playersaway:
        if x == "Manager":
            continue
        if x.pos != "COACH":
            x.form = player_form(team_form_away)
            x.ovr += x.form
            away_ovr_list.append(x.ovr)

    away_ovr = round(sum(away_ovr_list) / len(away_ovr_list))


    ### Home team stats
    team_name_home = t_info.split(",")[0]
    team_form_home = t_info.split(",")[3]

    teamsname = Teams(team_name_home, team_name_away)
    home_man = playershome[0]
    home_ovr_list = []

    for x in playershome:
        if x == "Manager":
            continue
        if x.pos != "COACH":
            x.form = player_form(team_form_home)
            x.ovr += x.form
            home_ovr_list.append(x.ovr)

    home_ovr = round(sum(home_ovr_list) / len(home_ovr_list))

    ### Matchs initialisation
    score_home = 0
    score_away = 0
    score = Score(score_home, score_away)
    num_events = 120

    home_bonus = round(home_ovr - away_ovr)
    away_bonus = round(away_ovr - home_ovr)
    bonus = abs(home_bonus)

    note = randint(1, 100)
    if note <= 10:
        note = 1
    elif 10 < note <= 30:
        note = 2
    elif 30 < note <= 70:
        note = 3
    elif 70 < note <= 90:
        note = 4
    elif 90 < note:
        note = 5

    if bonus == 0:
        bonus = 1

    # % per minute to have an action, in fact it will be nb_actions / minutes
    nb_actions = 4 * note + randint(1, bonus)

    i = 0

    ### Lists of events (minutes, score_home, score_away)
    matchevents = []
    eventlist = []
    curevent = "\u200b"

    startPlayer = playershome[randint(1,5)]
    commentary = commentaries.getCommentary('matchStart', {'HOME_TEAM': teamsname.home, 'AWAY_TEAM': teamsname.away, 'START_PLAYER_NAME': startPlayer.displayName})

    def get_actions(team, player, status):
        ## Define scoring probabilities
        action = ""
        reverseteam = ""
        indice = 1
        whoreceiveaction = [20,40,60,80,100]
        receivePossession = ""
        receiveBall = ""
        whoreceiveinteam = ""
        whoreceiveinrevteam = ""
        assist = ""
        success = 0

        number = randint(1, 100)
        for x in whoreceiveaction:
            if number > x:
                indice += 1

        if team == "home":
            reverseteam = "away"
            teamname = team_name_home
            if player == "":
                who = playershome[indice]
            else:
                who = player
            if playershome[indice] != player:
                whoreceiveinteam = playershome[indice]
                whoreceiveinrevteam = playersaway[indice]
            else:
                whoreceiveinrevteam = playersaway[randint(1,5)]
                if indice == 1:
                    whoreceiveinteam = playershome[indice + randint(1,4)]
                else:
                    whoreceiveinteam = playershome[indice-1]

        if team == "away":
            reverseteam = "home"
            teamname = team_name_away
            if player == "":
                who = playersaway[indice]
            else:
                who = player
            if playersaway[indice] != player:
                whoreceiveinteam = playersaway[indice]
                whoreceiveinrevteam = playershome[indice]
            else:
                whoreceiveinrevteam = playershome[randint(1, 5)]
                if indice == 1:
                    whoreceiveinteam = playersaway[indice + randint(1,4)]
                else:
                    whoreceiveinteam = playersaway[indice-1]

        print(str(who.ovr)+" vs "+str(whoreceiveinrevteam.ovr))
        withdef = randint(1,5)
        maxchance = 100
        delta = 0
        if withdef > 2:
            delta = who.ovr - whoreceiveinrevteam.ovr
        trying = randint(1, maxchance + delta)

        if status == "NoShot":
            action = randint(1,3)
            if action > 1:
                action = "Pass"
                if trying > 30:
                    success = 1
            else:
                action = "Dribble"
                if trying > 30:
                    success = 1
            if success == 1:
                status = "CanShoot"
                receivePossession = team
                if action == "Pass":
                    receiveBall = whoreceiveinteam
                    assist = player
                else:
                    receiveBall = who
            else:
                status = "NoShot"
                receivePossession = reverseteam
                receiveBall = whoreceiveinrevteam
        elif status == "CanShoot":
            action = "Shoot"
            shootzone = randint(1,3)
            if shootzone > 2:
                if trying > 60:
                    success = 2
            else:
                if trying > 30:
                    success = 1
            if success > 0:
                status = "NoShot"
                receivePossession = reverseteam
                receiveBall = whoreceiveinrevteam
            else:
                status = "MissShot"
                receivePossession = ""
                receiveBall = ""
        elif status == "MissShot":
            action = "Rebound"
            if trying > 10:
                success = 1
                status = "CanShoot"
                receivePossession = team
                receiveBall = who
            else:
                status = "NoShot"
                receivePossession = reverseteam
                receiveBall = whoreceiveinrevteam


        return who, teamname, action, team, success, status, receiveBall, receivePossession, assist

    async def register_goals(player, team, sort):
        # Update f_goals

        if event == "no":
            pfile = open(f_goals, "r+")
        else:
            pfile = open(config["dataPath"] + "goals_" + event + ".csv", "r+")

        playerfile = pfile.readlines()
        playerlist = []
        newgoals = 1
        status = 0

        if len(playerfile) > 0:
            if sort == "byPlayer":
                new_line = str(newgoals) + "," + team + "," + player + ",\n"
                for line in playerfile:
                    fteam = line.split(",")[1]
                    fplayer = line.split(",")[2]

                    if (fplayer == player) and (fteam == team):
                        fgoals = int(line.split(",")[0])
                        newgoals = fgoals + 1
                        new_line = str(newgoals) + "," + team + "," + player + ",\n"
                        replace = line.replace(line, new_line)
                        line = replace
                        if "," not in line:
                            line = ",,,,\n"
                        status = 1

                    playerlist.append(line)

            elif sort == "byTeam":
                new_line = str(newgoals) + ","+ team + ",\n"
                for line in playerfile:
                    fteam = line.split(",")[1]

                    if fteam == team:
                        fgoals = int(line.split(",")[0])
                        newgoals = fgoals + 1
                        new_line = str(newgoals) + ","+ team + ",\n"
                        replace = line.replace(line, new_line)
                        line = replace
                        if "," not in line:
                            line = ",,,,\n"
                        status = 1

                    playerlist.append(line)

        if status == 0:
            pfile.write(new_line)
        else:
            pfile.seek(0)
            pfile.truncate(0)
            pfile.writelines(playerlist)


        pfile.close()

    #### Start of the simulation ###############
    qtime = 1
    qmin = 0
    shootstatus = "NoShot"
    hasPossession = ""
    hasBall = ""
    lastpass = ""

    matchevent = MatchEvent(teamsname, score, curevent, commentary, qtime, qmin, note)
    eventlist.append(matchevent)

    while i < num_events:

        minutes = i // 3
        qtime = 1 + (i // 30)
        qmin = minutes % 10

        ## Recheck team value (can change during game)
        home_ovr_list = []
        curevent = "\u200b"

        for x in playershome:
            if x == "Manager":
                continue
            if x.pos != "COACH":
                home_ovr_list.append(x.ovr)

        home_ovr = round(sum(home_ovr_list) / len(home_ovr_list))

        away_ovr_list = []
        for x in playersaway:
            if x == "Manager":
                continue
            if x.pos != "COACH":
                away_ovr_list.append(x.ovr)

        away_ovr = round(sum(away_ovr_list) / len(away_ovr_list))
        home_bonus = round(home_ovr - away_ovr)

        ## Give a balance between the 2 teams (if same OVR : 1-50 and 51-100 to find who makes the action)
        if hasPossession == "":
            ratio = round(50 + home_bonus/5)
            who_attack = randint(1, 100)
            print(str(ratio) + " "+str(who_attack))
            if who_attack > ratio:
                hasPossession = "away"
            else:
                hasPossession = "home"

        i += 1
        ### Actions
        who, whoTeam, action, team, success, shootstatus, receiveBall, receivePossession, assist = get_actions(hasPossession, hasBall, shootstatus)
        hasPossession = receivePossession
        hasBall = receiveBall
        if action == "Pass":
            lastpass = assist
        elif action != "Shoot":
            lastpass = ""

        ## Define who have the ball after action
        whoplay = who.displayName

        if action == "Shoot":

            commentary = commentaries.getCommentary('shoot', {'PLAYER_NAME': whoplay, 'PLAYER_TEAM': whoTeam})
            matchevent = MatchEvent(teamsname, score, curevent, commentary, qtime, qmin, note)
            eventlist.append(matchevent)

            nbpoints = 2
            if success == 2:
                nbpoints = 3

            if success > 0:
                who.points += nbpoints
                if lastpass != "":
                   lastpass.assists += 1

                if team == "home":
                    score_home += nbpoints
                    score = Score(score_home, score_away)
                    if event != "versus":
                        await register_goals(whoplay, teamsname.home, leads)

                else:
                    score_away += nbpoints
                    score = Score(score_home, score_away)
                    if event != "versus":
                        await register_goals(whoplay, teamsname.away, leads)


                curevent = Event("goal", whoplay, whoTeam, qtime, qmin)
                if success == 1:
                    commentary = commentaries.getCommentary('goal',
                                                                {'PLAYER_NAME': whoplay, 'PLAYER_TEAM': whoTeam})
                else:
                    commentary = commentaries.getCommentary('3goal',
                                                                {'PLAYER_NAME': whoplay, 'PLAYER_TEAM': whoTeam})

            else:
                commentary = commentaries.getCommentary('missedShot', {'PLAYER_NAME': whoplay, 'PLAYER_TEAM': whoTeam})


        elif action == "Pass":
            commentary = commentaries.getCommentary('pass', {'PLAYER_NAME': whoplay, 'PLAYER_NAME2': hasBall.displayName, 'PLAYER_TEAM': whoTeam})

            if success == 0:
                #who.ovr = who.ovr - 3
                commentary = commentaries.getCommentary('missedPass', {'PLAYER_NAME': whoplay, 'PLAYER_NAME2': hasBall.displayName, 'PLAYER_TEAM': whoTeam})

        elif action == "Dribble":
            commentary = commentaries.getCommentary('dribble', {'PLAYER_NAME': whoplay, 'PLAYER_TEAM': whoTeam})
            if success == 0:
                #who.ovr = who.ovr - 3
                commentary = commentaries.getCommentary('missedDribble', {'PLAYER_NAME': whoplay, 'PLAYER_NAME2': hasBall.displayName, 'PLAYER_TEAM': whoTeam})

        elif action == "Rebound":
            who.rebounds += 1
            commentary = commentaries.getCommentary('rebound', {'PLAYER_NAME': whoplay, 'PLAYER_TEAM': whoTeam})

        else:
            commentary = commentaries.getCommentary('noAction')

        matchevents.append(str(i) + "," + str(score_home) + "," + str(score_away))

        matchevent = MatchEvent(teamsname, score, curevent, commentary, qtime, qmin, note)
        eventlist.append(matchevent)

    ### Note review
    if (int(score_away + score_home) <= 1) and (note > 1):
        note = note - 1
    elif int(score_away + score_home) > 3 and (note < 3):
        note = note + 1
    elif (int(score_away + score_home) <= 2) and (note > 3):
        note = note - 1

    ### Points Leaderboard
    async def update_points_leaderboard(team, addpoints):
        status = 0
        points_file = open(f_points, "r+")
        lines = []
        for line in points_file:
            fteam = line.split(",")[1]
            if fteam == team:
                points = int(line.split(",")[0])
                points = points + addpoints
                new_line = str(points) + "," + team + ",\n"
                replace = line.replace(line, new_line)
                line = replace
                if "," not in line:
                    line = ",,,,\n"
                status = 1
            lines.append(line)
        if status == 0:
            new_line = str(addpoints) + "," + team + ",\n"
            points_file.write(new_line)
        else:
            points_file.seek(0)
            points_file.truncate(0)
            points_file.writelines(lines)

    if event == "no":
        if score_home > score_away:
            await update_points_leaderboard(team_name_home, 3)
        elif score_home == score_away:
            await update_points_leaderboard(team_name_home, 1)

    commentaryKey = 'homeWin' if score_home > score_away else "awayWin" if score_home < score_away else "draw"
    commentary = commentaries.getCommentary(commentaryKey, {'HOME_TEAM': team_name_home, 'AWAY_TEAM': team_name_away})

    # Goal reset
    curevent = "\u200b"

    matchevent = MatchEvent(teamsname, score, curevent, commentary, qtime, qmin, note)
    eventlist.append(matchevent)

    return eventlist, playershome, playersaway


#### SIMULATE MATCHES ####
async def play(id, vs, events):
    user_id = str(id)
    eventlist, playershome, playersaway = await simulate(user_id, vs, events)

    home_name = eventlist[0].teams.home
    away_name = eventlist[0].teams.away
    commentary = eventlist[0].commentary

    description_start = "Welcome to the match !\nToday, *" + home_name + "* will face *" + away_name + "*.\n\nThe teams enter the " \
                                                                                                    "field... let's go! "
    description_default = "Welcome to the match !\nToday, *" + home_name + "* will face *" + away_name + "*.\n"

    note = int(eventlist[0].note)
    if note == 1:
        note = "⭐"
    elif note == 2:
        note = "⭐⭐"
    elif note == 3:
        note = "⭐⭐⭐"
    elif note == 4:
        note = "⭐⭐⭐⭐"
    elif note == 5:
        note = "⭐⭐⭐⭐⭐"

    default_color = 0xffff00
    embedlist = []

    nogoal = "\u200b"
    hgoal = nogoal
    agoal = nogoal
    hcard = nogoal
    acard = nogoal
    lastcommentaries = "\u200b"

    i = 0

    oldcommentaries = []

    for x in eventlist:

        lastevent1 = eventlist[i - 1].commentary
        minutes1 = eventlist[i - 1].minutes

        commentary = x.commentary

        if i > 1:
            if lastevent1 != "---":
                oldcommentaries.append("("+str(minutes1)+"') " + lastevent1)

        if len(oldcommentaries) > 2:
            lastcommentaries = oldcommentaries[-1] + "\n" + oldcommentaries[-2] + "\n" + oldcommentaries[-3]
        elif len(oldcommentaries) > 1:
            lastcommentaries = oldcommentaries[-1] + "\n" + oldcommentaries[-2]
        elif len(oldcommentaries) > 0:
            lastcommentaries = oldcommentaries[-1]

        i += 1

        minutes = x.minutes
        quarter = x.quarter

        if (int(minutes) == 1) and (quarter == 1):
            description = description_start
        elif x == eventlist[len(eventlist) - 1]:
            description = "The referee whistles the end of the game !"
        else:
            description = description_default

        home_score = str(x.score.home)
        away_score = str(x.score.away)
        embedscore = discord.Embed(
            title='Match Day', color=default_color, description=description)
        embedscore.add_field(name=home_name+" - "+away_name, value=home_score+" - "+away_score, inline=True)
        embedscore.add_field(name="QT " + str(quarter), value="MIN : "+str(minutes) + "'", inline=True)
        #embedscore.add_field(name=away_name, value=str(away_score), inline=True)
        embedscore.add_field(name="Commentary", value=commentary, inline=False)
        if len(oldcommentaries) > 0:
            embedscore.add_field(name="\u200b", value=lastcommentaries, inline=False)
        if i == len(eventlist):
            #embedscore.add_field(name=playershome[1].displayName, value=playershome[1].points, inline=False)
            embedscore.add_field(name="Match Note", value=note, inline=False)

        embedlist.append(embedscore)

    return embedlist, playershome, playersaway
