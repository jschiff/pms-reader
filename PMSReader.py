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

    def read_provider_records(self, rawdata):
        # TODO
        return ''

    # Read patient records from a string
    def read_patient_record_string(self, string_data):
        with StringIO(string_data) as stream:
            return self.read_patient_record_stream(stream)

    # Read patient records from a stream
    def read_patient_record_stream(self, raw_data):
        print(type(raw_data))
        # Now we're not thread safe
        self.__uniques = {}
        records = []

        # Ignore the header and initial padding
        raw_data.read(PMSReader.RECORD_SIZE)

        sectiona = raw_data.read(PMSReader.SECTION_A_SIZE)
        while sectiona != '' and sectiona != PMSReader.PADDING_SECTION_A:
            record = PatientRecord()
            sectionb = raw_data.read(PMSReader.SECTION_B_SIZE)
            sectionc = raw_data.read(PMSReader.SECTION_C_SIZE)
            sectiond = raw_data.read(PMSReader.SECTION_D_SIZE)
            sectione = raw_data.read(PMSReader.SECTION_E_SIZE)
            sectionf = raw_data.read(PMSReader.SECTION_F_SIZE)
            sectiong = raw_data.read(PMSReader.SECTION_G_SIZE)
            sectionh = raw_data.read(PMSReader.SECTION_H_SIZE)
            sectioni = raw_data.read(PMSReader.SECTION_I_SIZE)
            sectionj = raw_data.read(PMSReader.SECTION_J_SIZE)
            sectionk = raw_data.read(PMSReader.SECTION_K_SIZE)
            sectionl = raw_data.read(PMSReader.SECTION_L_SIZE)
            sectionm = raw_data.read(PMSReader.SECTION_M_SIZE)
            sectionn = raw_data.read(PMSReader.SECTION_N_SIZE)
            sectiono = raw_data.read(PMSReader.SECTION_O_SIZE)
            sectionp = raw_data.read(PMSReader.SECTION_P_SIZE)

            # Save the data we care about.
            record.id = self.format_as_hex_string(sectiona)
            record.firstName = self.normalize_text(sectionc)
            record.lastName = self.normalize_text(sectiond)
            record.phone1 = self.normalize_text(sectionh)
            record.phone2 = self.normalize_text(sectioni)
            record.gender = self.normalize_text(sectionj)
            record.gender = None if not record.gender else record.gender[0]

            records.append(record)

            # Prime for the next iteration
            sectiona = raw_data.read(PMSReader.SECTION_A_SIZE)

        return records

    def normalize_text(self, text):
        text = text.replace('\00', '').strip()
        return None if text == '' else text

    def format_as_hex_string(self, value):
        return ''.join(x.encode('hex') for x in value)
