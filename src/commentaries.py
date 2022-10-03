from random import choice

commentaries = {
    'matchStart': [
        "The match begins!",
        "The pitch looks perfect for today's game against *{HOME_TEAM}* and *{AWAY_TEAM}*",
        "Both *{HOME_TEAM}* and *{AWAY_TEAM}* are playing at a high level, we should be in for a thrilling game.",
        "The field conditions are less than ideal, let's see if that will have an impact on the game.",
        "Let's find out if *{AWAY_TEAM}* will be able to overcome *{HOME_TEAM}* in their fortress.",
        "The referee gets us underway in this match between *{HOME_TEAM}* & *{AWAY_TEAM}*.",
        "90 minutes plus added time are up and the referee blows his whistle.",
        "1 field, 2 teams, 22 players, 1 ball. Let's see what will happen now for this match between *{HOME_TEAM}* and *{AWAY_TEAM}*",
        "A lovely evening here as *{HOME_TEAM}* look to secure the win in front of their home crowd. *{START_PLAYER_NAME}* kicks things off and we are underway!",
        "*{AWAY_TEAM}* and *{HOME_TEAM}* are ready to battle it out in what should be an entertaining contest. *{START_PLAYER_NAME}* gets us underway.",
        "KICK OFF! The referee signals the start of the match and *{START_PLAYER_NAME}* get us underway."
    ],
    'homeWin': [
        "At home, *{HOME_TEAM}* wins the game against *{AWAY_TEAM}*",
        "**{HOME_TEAM}** makes a great match and overcomes *{AWAY_TEAM}*",
        "Dominant performance by *{HOME_TEAM}*, well deserved the win and the 3 points.",
        "Mission accomplished for *{HOME_TEAM}* against *{AWAY_TEAM}* !",
        "Full time! It's all over and *{HOME_TEAM}* fans are on their feet to applaud a very good performance by the hosts.",
        "FULL TIME! That's all the action for today, as *{HOME_TEAM}* defeat *{AWAY_TEAM}* in an action-packed encounter.",
        "FULL TIME! *{HOME_TEAM}* players celebrate their well-deserved victory over the visitors!",
        "Final whistle! *{HOME_TEAM}* prevail over *{AWAY_TEAM}* on their home turf."
    ],
    'awayWin': [
        "Away, *{AWAY_TEAM}* wins the game against *{HOME_TEAM}*",
        "**{AWAY_TEAM}** makes a great match and defeats *{HOME_TEAM}*",
        "It's full time and *{AWAY_TEAM}* have recorded a richly-deserved victory",
        "**{HOME_TEAM}** was surprised by *{AWAY_TEAM}* in this match !",
        "The referee blows the final whistle. A disappointing performance by the hosts sees *{AWAY_TEAM}* take this one!",
        "Final whistle! *{AWAY_TEAM}* comes out on top while the home side comes away empty-handed.",
        "Full Time! *{AWAY_TEAM}* players celebrate their well-deserved victory over the hosts today!",
        "Full time! That's all the action for today, as *{AWAY_TEAM}* defeat *{HOME_TEAM}* in an action-packed encounter."
    ],
    'draw': [
        "What a game!\n**{HOME_TEAM}** and *{AWAY_TEAM}* were at the same level today.",
        "Nothing to separate the 2 sides today.",
        "DRAW! No winners today as this hard-fought battle comes to a close.",
        "It's a draw! *{HOME_TEAM}* manage to defend home turf against a tough *{AWAY_TEAM}* side."
    ],
    'dominant': [
        "**{DOMINANT_TEAM}** is dominating the game!",
        "**{DOMINATED_TEAM}** don't see the light today!",
        "**{DOMINANT_TEAM}** have been absolutely dominant so far in this contest.",
        "**{DOMINANT_TEAM}** have taken control of this match. Can *{DOMINATED_TEAM}* hold on?",
        "This is becoming a one-sided affair with *{DOMINANT_TEAM}* now largely in control of the ball.",
        "**{DOMINANT_TEAM}** seem to have upped their intensity and it's unsettled *{DOMINATED_TEAM}*.",
        "**{DOMINATED_TEAM}** must be hoping *{DOMINANT_TEAM}* take their foot off the gas. They're struggling!",
        "**{DOMINANT_TEAM}** are toying with their opponents at this point."
    ],
    'shoot': [
        "**{PLAYER_NAME}** is in a good position and shoots...",
    ],
    'goal': [
        "🏀 2 points for *{PLAYER_TEAM}* by *{PLAYER_NAME}* !",
    ],
    '3goal': [
        "🏀 Woooo ! 3 points for *{PLAYER_TEAM}* by *{PLAYER_NAME}* !",
    ],
    'missedShot': [
        "What was that ?! Poor shot by *{PLAYER_NAME}*",
    ],
    'pass': [
        "*{PLAYER_TEAM}* : Pass from {PLAYER_NAME} to *{PLAYER_NAME2}*"
    ],
    'dribble': [
        "*{PLAYER_TEAM}* : Beautiful dribble from {PLAYER_NAME}"
    ],
    'missedPass': [
        "*{PLAYER_TEAM}* : Pass from {PLAYER_NAME} but *{PLAYER_NAME2}* intercepts !"
    ],
    'missedDribble': [
        "*{PLAYER_TEAM}* : Dribble from {PLAYER_NAME} but *{PLAYER_NAME2}* intercepts !"
    ],
    'rebound': [
        "*{PLAYER_TEAM}* : {PLAYER_NAME} takes the rebound."
    ],
    'noAction': [
        "---"
    ]
}

def getCommentary(actionType, replacements = {}):
  return choice(commentaries[actionType]).format(**replacements)
