import psycopg2
import psycopg2.extras

import recognition
import actions
import triggers
from shared import say, getGreeting
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
    # GRANT INSERT, UPDATE, SELECT, TRIGGER ON ALL TABLES IN SCHEMA public TO "home-automation";
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
convMode = None
# TODO Some arbitrary values, probably should check this
MAIN_LOOP_DELAY = 100
# Time in seconds before an incomplete command is aborted
COMMAND_TIMEOUT = 5
# This tracks the current action through calls
# to keep state if insufficient arguments
# are provided or confirmation needed
currentAction = None

def setConvMode(mode):
    global convMode
    convMode = mode
    shared.convMode = mode
    #recognition.convMode = ConvMode.LISTENING

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

def checkActions(phrase):
    """
    Return a list of actions that could match the given phrase
    """
    matches = []
    for act in db['actions']:
        # Check if potential match
        if act['trigger_word'] in phrase:
            obj = act['function']()
            # If deeper analysis fails, ignore it
            if not obj.phraseMatch(phrase):
                continue
            # Otherwise, add it to matches
            else:
                matches.append(obj)
    return matches

def handleAction(phrase):
    """
    Responsible for ensuring the passed-in phrase is handled correctly
    and parsing the output of a given action, including getting missing information
    """
    actions = checkActions(phrase)
    if len(actions) > 1:
        # TODO conflict resolution
        pass
    else:
        obj = actions[0]
        missingArgs = obj.checkArguments()
        if len(missingArgs) == 0:
            if not CONFIRM_ALL:
                obj.execute()
                setConvMode(ConvMode.FINISHING)
            else:
                setConvMode(ConvMode.REPROMPTING)
                # TODO create string of intended action
                # and inquire if it is correct
                pass
        else:
            setConvMode(ConvMode.REPROMPTING)
            # TODO query missing arguments
            pass
    
def parsePhrase(phrase):
    """
    Takes a spoken phrase and performs appropriate action based on current
    state and environment
    """
    # TODO will need to know room speech came from to direct output correctly
    # TODO set as variable in current action?
    if convMode == ConvMode.LISTENING:
        if MY_NAME in phrase:
            setConvMode(ConvMode.ACTIVE)
            # Check that a command was given in addition to name
            if phrase.count(' ') > 5:
                # Conversation state will be handled inside this function
                return handleAction(phrase)
            else:
                message = getGreeting(dbCursor)
                # TODO this will probably need an argument for output line
                say(message)
                return None
    elif convMode == ConvMode.ACTIVE:
        handleAction(phrase)
    elif convMode == ConvMode.CONFIRMING:
        tone = getTone(phrase)
        if tone == 'p':
            # TODO have arguments been checked?
            # Probably?
            currentAction.execute()
            setConvMode(ConvMode.FINISHING)
        elif tone == 'n':
            setConvMode(ConvMode.LISTENING)
            # TODO find a more elegant way to do this
            if 'amend' in phrase or 'change' in phrase or 'modify' in phrase:
                setConvMode(ConvMode.REPROMPTING)
                return currentAction
            else:
                return None
        elif tone == 'u':
            # TODO restate prompt
            pass
    elif convMode == ConvMode.REPROMPTING:
        currentAction.parsePhrase(phrase)
        if len(currentAction.checkArguments()) == 0:
            # TODO confirm phrase
            setConvMode(ConvMode.CONFIRMING)
        else:
            # TODO Get new missing arguments
            pass
    elif convMode == ConvMode.FINISHING:
        actions = checkActions(phrase)
        if len(actions) == 0:
            setConvMode(ConvMode.LISTENING)
            return None
        else:
            handleAction(phrase)
        pass

def respond():
    """
    Determine appropriate response and say it
    """
    # TODO will need to know room speech came from to direct output correctly
    pass

def checkTriggers():
    """
    Check if any database trigger conditions are met
    and perform appropriate action if they are
    """
    # TODO this
    pass

def checkTimeouts():
    """
    Check timeout for conversation mode and reprompt if necessary
    or cancel action
    """
    # The action start time should be stored inside its object
    # TODO this
    pass

while True:
    # Check speech, act on it if necessary
    phrase = recognition.getSpeech()
    if phrase:
        currentAction = parsePhrase(phrase)

    # Check other conditions/states
    checkTriggers()
    checkTimeouts()

    sleep(MAIN_LOOP_DELAY)
