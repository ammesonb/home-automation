import recognition
import actions
import triggers
from recognition import ConvMode
from time import sleep

# TODO
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
    pass

def loadData():
    """
    Loads all information stored in database to global variables
    """
    pass

openDBConnection()
loadData()
recognition.initSphinx()

def parsePhrase(phrase):
    # TODO will need to know room speech came from
    if conv_mode == ConvMode.LISTENING:
        if name in phrase:
            setConvMode(ConvMode.ACTIVE)
            # TODO Parse command
            pass
    elif conv_mode == ConvMode.ACTIVE:
        # TODO Parse command
        pass
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
    sleep(MAIN_LOOP_DELAY)
