import discord
import requests
from config import config
import players


#### Show NFT players
async def get(id, indice):

    nations_prefix = {
        'ALGERIA': 'dz',
        'ARGENTINA': 'ar',
        'AUSTRALIA': 'au',
        'AUSTRIA': 'at',
        'BELGIUM': 'be',
        'BRAZIL': 'br',
        'CANADA': 'ca',
        'CAMEROON': 'cm',
        'CHILE': 'cl',
        'COLOMBIA': 'co',
        'COSTA_RICA': 'cr',
        'CROATIA': 'hr',
        'CZECH_REPUBLIC': 'cz',
        'DENMARK': 'dk',
        'ECUADOR': 'ec',
        'ENGLAND': 'gb',
        'EGYPT': 'eg',
        'FRANCE': 'fr',
        'GERMANY': 'de',
        'HUNGARY': 'hu',
        'KOREA_REPUBLIC': 'kr',
        'ITALY': 'it',
        'IRAN': 'ir',
        'JAPAN': 'jp',
        'MEXICO': 'mx',
        'MOROCCO': 'ma',
        'NETHERLANDS': 'nl',
        'NIGERIA': 'ng',
        'NORWAY': 'no',
        'PARAGUAY': 'py',
        'PERU': 'pe',
        'POLAND': 'pl',
        'PORTUGAL': 'pt',
        'UKRAINE': 'ua',
        'REPUBLIC_OF_IRELAND': 'ie',
        'ROMANIA': 'ro',
        'RUSSIA': 'ru',
        'SAUDI_ARABIA': 'sa',
        'SCOTLAND': 'gb',
        'SENEGAL': 'sn',
        'SERBIA': 'rs',
        'SLOVAKIA': 'sk',
        'SPAIN': 'es',
        'SWITZERLAND': 'ch',
        'SWEDEN': 'se',
        'TUNISIA': 'tn',
        'TURKEY': 'tr',
        'UNITED_STATES': 'us',
        'URUGUAY': 'uy',
        'WALES': 'gb'

    }

    host = config["apiUrl"] + "/users/discord/"
    user_id = str(id)
    link = host+user_id+"/players"
    headers = {
        'x-api-key': config["apiKey"]
    }
    getnft = requests.get(link, headers=headers)
    nfts = getnft.json()

    i = 0

    playerslist = []
    formatlist = []
    embeddesclist = []
    embeddescription = ""

    while i < len(nfts):
        nationality = nfts[i]['metadata']['nationalities'][0]
        try:
            nation = nations_prefix[nationality]
        except:
            nation = nationality
        positions = nfts[i]['metadata']['positions'][0]
        ovr = int(nfts[i]['metadata']['overall'])
        firstName = nfts[i]['metadata']['firstName']
        lastName = nfts[i]['metadata']['lastName']
        displayName = firstName + " " + lastName

        if ovr >= 85:
            rarity = "legend"
        elif ovr >= 75:
            rarity = "rare"
        elif ovr >= 65:
            rarity = "uncommon"
        else:
            rarity = "common"

        embeddescription = embeddescription + ":flag_" + nation + ":`" + positions + "  " + str(ovr) + "`" + rarity + " *" + displayName + "*\n"
        playerslist.append(nation+","+positions+","+str(ovr)+","+displayName+","+rarity)

        i += 1

        if (i % 5 == 0) or (i == len(nfts)):
            formatlist.append(playerslist)
            playerslist = []
            embeddesclist.append(embeddescription)
            embeddescription = ""

    if int(indice) > len(embeddesclist):
        indice = len(embeddesclist) - 1
    elif int(indice) < 0:
        indice = 0

    return formatlist

async def scout(id, name, ovr, pos, nat, rarity):
    user_id = str(id)
    p_info = await players.get(user_id)

    positions = {
        'GK': 1,
        'LB': 2,
        'LWB': 2,
        'CB': 3,
        'RB': 5,
        'RWB': 5,
        'CDM': 6,
        'CM': 7,
        'CAM': 7,
        'AM': 7,
        'LW': 9,
        'LM': 9,
        'RW': 10,
        'RM': 10,
        'CF': 11,
        'ST': 11,
        'FW': 11
    }

    name = name
    ovr = int(ovr)
    pos = pos
    number = positions[pos]
    nat = nat
    nft = "1"
    rarity = rarity

    if rarity == "common":
        rarity_flag = "⚪"
    elif rarity == "uncommon":
        rarity_flag = "🟢"
    elif rarity == "rare":
        rarity_flag = "🔵"
    elif rarity == "legend":
        rarity_flag = "🟣"

    if number in (3, 4):
        ovr3 = p_info[3].ovr
        ovr4 = p_info[4].ovr
        if ovr3 < ovr4:
            old_name = p_info[3].displayName
            old_ovr = p_info[3].ovr
            old_pos = p_info[3].pos.upper()
            old_nat = p_info[3].nat
            number = 3
        else:
            old_name = p_info[4].displayName
            old_ovr = p_info[4].ovr
            old_pos = p_info[4].pos.upper()
            old_nat = p_info[4].nat
            number = 4
    elif number in (7, 8):
        ovr6 = p_info[7].ovr
        ovr7 = p_info[8].ovr
        if ovr6 < ovr7:
            old_name = p_info[7].displayName
            old_ovr = p_info[7].ovr
            old_pos = p_info[7].pos.upper()
            old_nat = p_info[7].nat
            number = 7
        else:
            old_name = p_info[8].displayName
            old_ovr = p_info[8].ovr
            old_pos = p_info[8].pos.upper()
            old_nat = p_info[8].nat
            number = 8
    else:
        old_name = p_info[number].displayName
        old_ovr = p_info[number].ovr
        old_pos = p_info[number].pos.upper()
        old_nat = p_info[number].nat

    playerinfo = []
    playerinfo.append(number)
    playerinfo.append(name)
    playerinfo.append(ovr)
    playerinfo.append(pos)
    playerinfo.append(nat)
    playerinfo.append(nft)
    playerinfo.append(rarity)

    i = int(number)
    default_color = 0xffff00

    embedplayer = discord.Embed(
        title=name, description="You find a new player !", color=default_color)
    embeddescription = ":flag_" + nat + ":`" + str(i) + " - " + pos + " " + str(ovr) + "` " + rarity_flag + " *" + name + "*\n"
    oldplayer = ":flag_" + old_nat + ":`" + str(i) + " - " + old_pos + " " + str(old_ovr) + "` ~~" + old_name + "~~\n"

    embedplayer.add_field(name="New player", value=embeddescription)
    embedplayer.add_field(name="Player you will remove", value=oldplayer, inline=False)

    return embedplayer