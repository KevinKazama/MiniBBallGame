from dotenv import dotenv_values

dotenvValues = dotenv_values("../.env")

config = {
    "apiUrl": dotenvValues["API_URL"],
    "apiKey": dotenvValues["API_KEY"],
    "botToken": dotenvValues["BOT_TOKEN"],
    "adminId": dotenvValues["ADMIN_ID"].split(","),
    "gameChan": dotenvValues["GAME_CHAN"].split(","),
    "cooldown_scout": dotenvValues["CD_SCOUT"],
    "cooldown_match": dotenvValues["CD_MATCH"],
    "dataPath": "../data/",
}
