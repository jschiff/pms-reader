# -*- coding: utf-8 -*-
from PatientRecord import PatientRecord
from StringIO import StringIO
import struct


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
            rawdata.read(PMSReader.SECTION_B_SIZE)
            sectionc = rawdata.read(PMSReader.SECTION_C_SIZE)
            sectiond = rawdata.read(PMSReader.SECTION_D_SIZE)
            rawdata.read(PMSReader.SECTION_E_SIZE)
            rawdata.read(PMSReader.SECTION_F_SIZE)
            rawdata.read(PMSReader.SECTION_G_SIZE)
            sectionh = rawdata.read(PMSReader.SECTION_H_SIZE)
            sectioni = rawdata.read(PMSReader.SECTION_I_SIZE)
            sectionj = rawdata.read(PMSReader.SECTION_J_SIZE)
            rawdata.read(PMSReader.SECTION_K_SIZE)
            sectionl = rawdata.read(PMSReader.SECTION_L_SIZE)
            rawdata.read(PMSReader.SECTION_M_SIZE)
            rawdata.read(PMSReader.SECTION_N_SIZE)
            sectiono = rawdata.read(PMSReader.SECTION_O_SIZE)
            rawdata.read(PMSReader.SECTION_P_SIZE)


            record.id = self.extract16ByteId(sectiona)
            record.firstName = sectionc.strip()
            record.lastName = sectiond.strip()
            record.phone1 = sectionh.strip()
            record.phone2 = sectioni.strip()
            record.gender = sectionj.strip()[0]

            # Checking for uniqueness of various sections to see if any can serve as the record id...
            self.checkUniqueness(sectiona, 'a', len(records))
            self.checkUniqueness(sectionj, 'j', len(records))
            self.checkUniqueness(sectionl, 'l', len(records))
            self.checkUniqueness(sectiono, 'o', len(records))
            records.append(record)

            # Prime for the next iteration
            sectiona = rawdata.read(PMSReader.SECTION_A_SIZE)

        print('total entries: ' + str(len(records)))

        return records

    def checkUniqueness(self, value, section, recordcount):
        sectionunique = self.__uniques.get(section, {})
        self.__uniques[section] = sectionunique

        if sectionunique.get(value, False):
            print "Found duplicate value '" + str(value) + "' in section " + section + " from " + str(sectionunique[value]) + " at " + str(recordcount)
        else:
            sectionunique[value] = recordcount

    def extract16ByteId(self, value):
        return struct.unpack('QQ', value)
