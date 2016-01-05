class Action():
    def __init__(self):
        self.arguments = {}

    def phraseMatch(self, phrase):
        """
        Actions must provide a method to check a given phrase to see
        if it satisfies its base requirements, but not necessarily
        fully parse it
        """
        return False

    def execute(self):
        """
        Should check if arguments are valid and execute the action
        Return a boolean indicating success
        """
        if not self.checkArguments(): return False

    def checkArguments(self):
        """
        An inherited method that child classes should fill out
        Returns an array of arguments keys that are missing and
        must be provided to execute the action
        """
        return []

    def provideMissingArguments(self, args):
        """
        Update arguments for action using given dict
        """
        for arg in args.keys():
            self.arguments[arg] = args[arg]
