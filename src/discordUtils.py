def formatDateTimeForDiscord(dateTime, format = "T"):
    if (isinstance(dateTime, str)):
        return(dateTime)
    timestamp = round(dateTime.timestamp())
    return("<t:" + str(timestamp) + ":" + format + ">")
