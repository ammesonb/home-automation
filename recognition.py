import enum

class ConvMode(enum.Enum):
    # Listening for name/event, default
    LISTENING = 0
    # Heard name, listening for command
    ACTIVE = 1
    # Command parsed, waiting to confirm
    CONFIRMING = 2
    # Waiting for more information
    WAITING = 3
    # Occurs after a timeout of the prior three modes
    REPROMPTING = 4
    # Listening for acknowledgement of completion
    # This can time out safely
    FINISHING = 5

def initSphinx():
    """
    Start CMU Sphinx recognizer/integration
    """
    # TODO this
    pass

def getSpeech():
    """
    Responsible for returning a phrase from the CMU Sphinx voice recognition
    software
    """
    # TODO CMU sphinx integration here
    # Will it block?
    phrase = 'some string'
    # TODO May need to append text instead of parsing as is - how to tell?
    # Just collect a few seconds of text?
    return phrase
