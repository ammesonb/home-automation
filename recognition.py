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

