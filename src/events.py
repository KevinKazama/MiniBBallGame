from config import config

## Event (name, desc, status)
f_events = config["dataPath"] + "events.csv"

class Event:
    def __init__(self, code, name, desc, status, kind, opponent, leaderboard, reward):
        self.code = code
        self.name = name
        self.desc = desc
        self.status = status
        self.kind = kind
        self.opponent = opponent
        self.leaderboard = leaderboard
        self.reward = reward

async def get(i):
    with open(f_events, "r") as tevents:
        eventfile = tevents.readlines()
        eventlist = []

        for event in eventfile:
            code = event.split(",")[0]
            name = event.split(",")[1]
            desc = event.split(",")[2]
            status = event.split(",")[3]
            kind = event.split(",")[4]
            opponent = event.split(",")[5]
            leaderboard = event.split(",")[6]
            reward = event.split(",")[7]

            if int(status) > 1:
                continue

            if i == "all":
                mevent = Event(code, name, desc, status, kind, opponent, leaderboard, reward)
                eventlist.append(mevent)
            elif i == kind:
                mevent = Event(code, name, desc, status, kind, opponent, leaderboard, reward)
                eventlist.append(mevent)

        return eventlist

async def getbyCode(i):
    with open(f_events, "r") as tevents:
        eventfile = tevents.readlines()
        eventlist = []

        for event in eventfile:
            code = event.split(",")[0]
            name = event.split(",")[1]
            desc = event.split(",")[2]
            status = event.split(",")[3]
            kind = event.split(",")[4]
            opponent = event.split(",")[5]
            leaderboard = event.split(",")[6]
            reward = event.split(",")[7]

            if int(status) > 1:
                continue

            if i == code:
                mevent = Event(code, name, desc, status, kind, opponent, leaderboard, reward)
                eventlist.append(mevent)

        return eventlist
