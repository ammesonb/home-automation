class Action():
    def __init__(self, function):
        self.arguments = {}
        self.function = function

    def execute(self):
        if not self.checkArguments(): return

    def checkArguments(self):
        return True

    def provideMissingArguments(self):
        pass

def determineAction(phrase):
    """
    Uses keywords and actions loaded from database to determine
    what should be done for a given phrase
    Returns a dictionary with action database entry and parameters for the function
    If not enough information, will set an error flag in the dict and provide
    an error message
    """
    pass
