import datetime
from config import config

on_cooldown_scout = {}
on_cooldown_match = {}

cooldown_scout = config["cooldown_scout"]
cooldown_match = config["cooldown_match"]

def end_cooldown(user, cd_date, cd_dict, cd_name):
    now = datetime.datetime.now()

    if cd_name == "scout":
        cooldown = int(cooldown_scout)
    elif cd_name == "match":
        cooldown = int(cooldown_match)

    if now - datetime.timedelta(minutes=cooldown) > cd_date:
        cd_dict.pop(user)
        return("no")
    else:
        cdtime = cd_date + datetime.timedelta(minutes=cooldown)
        return(cdtime)


def check(user):

    cd_list = {}

    if (user in on_cooldown_scout.keys()):
        cd_date = on_cooldown_scout[user]
        cd_end = end_cooldown(user, cd_date, on_cooldown_scout, cd_name="scout")
        if cd_end != "no":
            cd_list["scout"] = cd_end

    if (user in on_cooldown_match.keys()):
        cd_date = on_cooldown_match[user]
        cd_end = end_cooldown(user, cd_date, on_cooldown_match, cd_name="match")
        if cd_end != "no":
            cd_list["match"] = cd_end

    return(cd_list)

def add_cd_scout(user):
    on_cooldown_scout[user] = datetime.datetime.now()

def add_cd_match(user):
    on_cooldown_match[user] = datetime.datetime.now()
