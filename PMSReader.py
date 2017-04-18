# -*- coding: utf-8 -*-
from PatientRecord import PatientRecord
from StringIO import StringIO


class PMSReader:
    RECORD_SIZE = 2008
    # Record ID
    SECTION_A_SIZE = 16
    SECTION_B_SIZE = 14
    # First name
    SECTION_C_SIZE = 32
    # Last name
    SECTION_D_SIZE = 16
    SECTION_E_SIZE = 16
    SECTION_F_SIZE = 82
    SECTION_G_SIZE = 11
    # Phone number
    SECTION_H_SIZE = 20
    # Also a phone number
    SECTION_I_SIZE = 55
    # ID that contains gender information
    SECTION_J_SIZE = 12
    SECTION_K_SIZE = 104
    SECTION_L_SIZE = 7
    SECTION_M_SIZE = 624
    SECTION_N_SIZE = 370
    SECTION_O_SIZE = 36
    SECTION_P_SIZE = 593

    PADDING_SECTION_A = '\xff' * SECTION_A_SIZE

    def __init__(self):
        self.__uniques = {}

    def readProviderRecords(self, rawdata):
        # TODO
        return ''

    # Read patient records from a string
    def readPatientRecordString(self, stringdata):
        with StringIO(stringdata) as stream:
            return self.readPatientRecordStream(stream)

    # Read patient records from a stream
    def readPatientRecordStream(self, rawdata):
        print(type(rawdata))
        # Now we're not thread safe
        self.__uniques = {}
        records = []

        # Ignore the header and initial padding
        rawdata.read(PMSReader.RECORD_SIZE)

        sectiona = rawdata.read(PMSReader.SECTION_A_SIZE)
        while sectiona != '' and sectiona != PMSReader.PADDING_SECTION_A:
            record = PatientRecord()
            sectionb = rawdata.read(PMSReader.SECTION_B_SIZE)
            sectionc = rawdata.read(PMSReader.SECTION_C_SIZE)
            sectiond = rawdata.read(PMSReader.SECTION_D_SIZE)
            sectione = rawdata.read(PMSReader.SECTION_E_SIZE)
            sectionf = rawdata.read(PMSReader.SECTION_F_SIZE)
            sectiong = rawdata.read(PMSReader.SECTION_G_SIZE)
            sectionh = rawdata.read(PMSReader.SECTION_H_SIZE)
            sectioni = rawdata.read(PMSReader.SECTION_I_SIZE)
            sectionj = rawdata.read(PMSReader.SECTION_J_SIZE)
            sectionk = rawdata.read(PMSReader.SECTION_K_SIZE)
            sectionl = rawdata.read(PMSReader.SECTION_L_SIZE)
            sectionm = rawdata.read(PMSReader.SECTION_M_SIZE)
            sectionn = rawdata.read(PMSReader.SECTION_N_SIZE)
            sectiono = rawdata.read(PMSReader.SECTION_O_SIZE)
            sectionp = rawdata.read(PMSReader.SECTION_P_SIZE)

            # Save the data we care about.
            record.id = self.formatAsHexString(sectiona)
            record.firstName = self.normalizeText(sectionc)
            record.lastName = self.normalizeText(sectiond)
            record.phone1 = self.normalizeText(sectionh)
            record.phone2 = self.normalizeText(sectioni)
            record.gender = self.normalizeText(sectionj)
            record.gender = None if not record.gender else record.gender[0]

            records.append(record)

            # Prime for the next iteration
            sectiona = rawdata.read(PMSReader.SECTION_A_SIZE)

        return records

    def normalizeText(self, text):
        text = text.replace('\00', '').strip()
        return None if text == '' else text

    def formatAsHexString(self, value):
        return ''.join(x.encode('hex') for x in value)
