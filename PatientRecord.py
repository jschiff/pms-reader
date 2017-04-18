class PatientRecord:
    def __init__(self):
        self.firstName = None
        self.lastName = None
        self.id = None
        self.phone1 = None
        self.phone2 = None
        self.gender = None

    def __str__(self):
        return '{0}: first: {1} last: {2} phone1: {3} phone2: {4} gender: {5}'.format(
            self.id,
            self.firstName,
            self.lastName,
            self.phone1,
            self.phone2,
            self.gender).encode('utf-8')
