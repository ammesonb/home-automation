from time import time
import hue_api

class Action():
    def __init__(self, keywords):
        self.arguments = {}
        self.keywords = keywords
        self.started = time()

    def phraseMatch(self, phrase):
        """
        Actions must provide a method to check a given phrase to see
        if it satisfies its base requirements, but not necessarily
        fully parse it
        """
        return False

    def parsePhrase(self, phrase):
        """
        Loads arguments from the given phrase
        Abstract method
        """
        pass

    def execute(self):
        """
        Should check if arguments are valid and execute the action
        Return a boolean indicating success
        """
        if not self.checkArguments(): return False

    def checkArguments(self):
        """
        An abstract method that child classes should fill out
        Returns an array of arguments keys that are missing and
        must be provided to execute the action
        """
        return []

class ControlLights(Action):
    # Args:
    # Room
    # Level OR Color
    def phraseMatch(self, phrase):
        """
        Since this controls lights, really just needs to match any one keyword
        """
        for kw in self.keyword:
            if kw in phrase:
                return True
        return False

    def parsePhrase(self, phrase):
        pass

    def execute(self):
        pass

    def checkArguments(self):
        # This only needs an amount since the room will default to
        # the one in which the request was received
        # While that may not have been the intended room, the request can then be
        # amended
        if self.arguments.has_key('amount'): return []
        return ['amount']
