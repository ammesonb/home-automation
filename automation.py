import psycopg2
import psycopg2.extras

import recognition
import actions
import triggers
from recognition import ConvMode
from time import sleep

# TODO
# Set up script
    # Path to pocketsphinx
    # Install postgres and python bindings
    # Install curl
    # Create automation database
    # Create user home-automation
    # Modify pg_hba.conf to require password for user on this database
    # Add privileges for user on database
    # Populate database
    # Select program name
    # Choose whether/where to save recordings
    # Enter Bluemix credentials
# Figure out room/microphone separation
# Actions
    # Facebook
    # Music
    # Movie/TV database
    # Texting
    # Lights
    # Chains
        # Get home
        # Wake up
        # Go to bed
        # Leave for work
    # Electrical outlets
    # Locks
        # Door
        # Garage?
        # Fridge
    # Change mode
    # Change confirmation
    # Add things generally to database?
# Triggers/events
    # Get home
    # Wake up
    # Go to bed
    # Leave for work
    # Room change for music
    # People arriving/leaving
        # OpenWRT associations/event handling?

# TODO Will pocketsphinx recognize this?
MY_NAME = "Proteus"
CONFIRM_ALL = True
MODE = "casual"
# TODO Some arbitrary values, probably should check this
MODE_CHANGE_TIMEOUT = 5000
MAIN_LOOP_DELAY = 100
last_mode_change = 0

def setConvMode(mode):
    global conv_mode
    conv_mode = mode
    #recognition.conv_mode = ConvMode.LISTENING

setConvMode(ConvMode.LISTENING)

def openDBConnection():
    """
    Opens connection to the PostgreSQL automation database
    with user home-automation and password home-automation
    """
    # TODO should password be randomly generated on setup instead?
    try:
        return psycopg2.connect("dbname='automation' user='home-automation' host='localhost' password='home-automation'")
    except:
        print "Unable to connect to the database"

db = {}
dbConn = openDBConnection()
dbCursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def loadData():
    """
    Loads all information stored in database to global variables
    """
    global db
    # Get local copies of actions, since need to know functions
    # and such when triggering events (and have human names for logging purposes)
    dbCursor.execute("SELECT * FROM actions")
    db['actions'] = dbCursor.fetchall()
    dbCursor.execute("SELECT * FROM events")
    db['events'] = dbCursor.fetchall()
    dbCursor.execute("SELECT * FROM chains")
    db['chains'] = dbCursor.fetchall()
    dbCursor.execute("SELECT * FROM chain_actions")
    db['chain_actions'] = dbCursor.fetchall()
    dbCursor.execute("SELECT * FROM keywords")
    db['keywords'] = dbCursor.fetchall()

loadData()
recognition.initSphinx()

def handleAction(phrase):
    """
    Responsible for ensuring the passed-in phrase is handled correctly
    and parsing the output of a given action, including getting missing information
    """
    actions.executeAction(phrase)
    
def parsePhrase(phrase):
    """
    Takes a spoken phrase and performs appropriate action based on current
    state and environment
    """
    # TODO will need to know room speech came from
    if conv_mode == ConvMode.LISTENING:
        if MY_NAME in phrase:
            setConvMode(ConvMode.ACTIVE)
            # Check that a command was given in addition to name
            if phrase.count(' ') > 5:
                handleAction(phrase)
            else:
                # TODO respond with greeting
                pass
    elif conv_mode == ConvMode.ACTIVE:
        handleAction(phrase)
    elif conv_mode == ConvMode.CONFIRMING:
        # TODO check for yes/no/affirming phrase
        pass
    elif conv_mode == ConvMode.REPROMPTING:
        # TODO Continue or abort previous action
        # TODO Need to know what that action is
        pass
    elif conv_mode == ConvMode.FINISHING:
        # TODO Check if this is a new command or just a 'thank you'
        # sort of response
        pass

def respond():
    """
    Determine appropriate response and say it
    """
    # TODO will need to know room speech came from
    pass

def checkTriggers():
    """
    Check if any database trigger conditions are met
    and perform appropriate action if they are
    """
    pass

def checkTimeouts():
    """
    Check timeout for conversation mode and reprompt if necessary
    or cancel action
    """
    pass

while True:
    # Check speech, act on it if necessary
    phrase = recognition.getSpeech()
    if phrase:
        parsePhrase(phrase)

    checkTriggers()
    checkTimeouts()
    # TODO should this be threaded?
    # Then maybe interrupts could be used instead of sleep?
        # Shared DB connection? Bad?
        # Conflicting choices - events and words, for instance?
        # Shared variables such as timeouts?
        # For hopefully-fast logic/decisions, is it really worth the overhead?

    sleep(MAIN_LOOP_DELAY)
