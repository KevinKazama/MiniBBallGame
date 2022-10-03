import requests
from config import config
import names
from random import randint, choice
import time

f_players = config["dataPath"] + "players.csv"

host = config["apiUrl"] + "/users/discord/"

pfile = open(f_players, "r+")
playerfile = pfile.readlines()
playerlist = []

for line in playerfile:
    found = 0
    player_infos = line.split(",")
    user_id = player_infos[3]
    isNFT = player_infos[5]
    if user_id != "593086239024873483":
        playerlist.append(line)
        continue
    if int(isNFT) == 1:
        playerName = player_infos[0]
        playerOvr = int(player_infos[1])
        playerPos = player_infos[2]
        playerNat = player_infos[4]
        print(playerName)
        link = host + user_id + "/players"
        headers = {
            'x-api-key': config["apiKey"]
        }
        try:
            getnft = requests.get(link, headers=headers)
            time.sleep(0.2)
            nfts = getnft.json()
        except:
            continue

        if found == 0:
            for x in nfts:
                firstName = x['metadata']['firstName']
                lastName = x['metadata']['lastName']
                displayName = firstName + " " + lastName
                if playerName == displayName:
                    ovr = int(x['metadata']['overall'])
                    if playerOvr == ovr:
                        found = 1
        if found == 0:
            playerName = names.get_full_name(gender='male')
            nationalities = ["gb", "us", "au", "fr", "ca", "es", "cu", "mx"]
            nat = choice(nationalities)
            ovr = randint(25, 30)
            new_line = playerName + "," + str(ovr) + "," + playerPos + "," + str(
                user_id) + "," + playerNat + "," + "0" + "," + "no" + ",\n"
            replace = line.replace(line, new_line)
            line = replace
            if "," not in line:
                line = ",,,,\n"

            print("player not found")
    playerlist.append(line)
# Replace entry in player file
pfile.seek(0)
pfile.truncate(0)
pfile.writelines(playerlist)
pfile.close()


