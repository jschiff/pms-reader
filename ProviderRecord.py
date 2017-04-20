class ProviderRecord:
    def __init__(self):
        self.id = None
        self.firstName = None
        self.lastName = None

    def __str__(self):
        return '{0}: first: {1} last: {2}'.format(
            self.id,
            self.firstName,
            self.lastName).encode('utf-8')
