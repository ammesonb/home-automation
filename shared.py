def say(phrase, save):
    """
    Speaks given phrase
    If save is True then will store recording
    """
    pass

def getGreeting(dbCursor):
    dbCursor.execute("SELECT * FROM greetings WHERE (SELECT create_ts_range()) && time_of_day ORDER BY random() LIMIT 1;")
    rows = dbCursor.fetchall()
    return rows[0]['phrase']
