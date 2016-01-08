def say(phrase, save):
    """
    Speaks given phrase
    If save is True then will store recording
    """
    # TODO this
    pass

def getGreeting(dbCursor):
    """
    Returns a random greeting appropriate for the time of day
    """
    dbCursor.execute("SELECT * FROM greetings WHERE (SELECT create_ts_range()) && time_of_day ORDER BY random() LIMIT 1;")
    rows = dbCursor.fetchall()
    return rows[0]['phrase']

def getTone(phrase):
    """
    Returns p/n/u for positive/negative/neutral tone
    """
    # TODO this
    return 'u'
