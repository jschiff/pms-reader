# -*- coding: utf-8 -*-
from PatientRecord import PatientRecord
from ProviderRecord import ProviderRecord
from StringIO import StringIO


def normalize_text(text):
    text = text.replace('\00', '').strip()
    return None if text == '' else text


def format_as_hex_string(value):
    return ''.join(x.encode('hex') for x in value)


class PMSReader:
    patients_data_section_lengths = [
        19,  # Record ID
        11,  # Title
        16,  # First name
        16,  # Middle name
        16,  # Last name
        16,
        82,
        11,
        20,  # Phone number
        19,  # Also a phone number
        36,  # Sometimes contains full name
        12,  # ID that contains gender information
        104,
        7,
        624,
        370,
        36,
        244,
        7,
        16,  # A uuid. This could be our id
        326
    ]

    providers_data_section_lengths = [
        13,  # Record ID
        16,  # Last name
        16,  # First name
        16,  # Middle name
        1086,  # The rest
    ]

    PADDING_SECTION_A = '\xff' * patients_data_section_lengths[0]

    def __init__(self):
        self.__uniques = {}

    def read_provider_record_string(self, string_data):
        with StringIO(string_data) as stream:
            return self.read_provider_record_stream(stream)

    def read_provider_record_stream(self, raw_data):
        data = self.extract_data(raw_data, PMSReader.providers_data_section_lengths)

        records = []
        for section_data in data:
            record = ProviderRecord()
            record.id = format_as_hex_string(section_data[0])
            record.lastName = normalize_text(section_data[1])
            record.firstName = normalize_text(section_data[2])
            records.append(record)

        return records

    # Read patient records from a string
    def read_patient_record_string(self, string_data):
        with StringIO(string_data) as stream:
            return self.read_patient_record_stream(stream)

    # Read patient records from a stream
    def read_patient_record_stream(self, raw_data):
        data = self.extract_data(raw_data, PMSReader.patients_data_section_lengths)

        records = []
        for section_data in data:
            # Save the data we care about.
            record = PatientRecord()
            record.id = format_as_hex_string(section_data[0])
            record.firstName = normalize_text(section_data[2])
            record.lastName = normalize_text(section_data[4])
            record.phone1 = normalize_text(section_data[8])
            record.phone2 = normalize_text(section_data[9])
            record.gender = normalize_text(section_data[11])
            record.gender = None if not record.gender else record.gender[0]

            records.append(record)
        return records

    def extract_data(self, raw_data, section_lengths):
        # Ignore the header and initial padding by skipping one section length of data.
        raw_data.read(sum(section_lengths))
        to_return = []

        while True:
            section_data = [None] * len(section_lengths)
            for i in range(0, len(section_lengths)):
                section_data[i] = (raw_data.read(section_lengths[i]))
                if section_data[i] == '':  # EOF reached
                    return to_return

            #  Don't add this record to the results if any of the sections are all 0xFF bytes
            #  This happens notably in the middle of some of some of the provider files.
            if not (any(all(x == '\xFF' for x in str(y[0])) for y in section_data)):
                to_return.append(section_data)

    #  Separates the data automatically by null bytes for analysis
    def analyze_data(self, raw_data):
        raw_data.read(sum(PMSReader.patients_data_section_lengths))

        null = True
        records = []
        record_index = 1
        while True:
            record_data = raw_data.read(sum(PMSReader.patients_data_section_lengths))
            if record_data == '':
                break

            sections = record_data.split('\x00')
            secdict = {}
            offset = 0
            for section in sections:
                secdict[offset + (record_index * sum(PMSReader.patients_data_section_lengths))] = section
                offset += len(section)

            secdict = {k: v for k, v in secdict.iteritems() if v != ''}

            records.append(secdict)
            record_index += 1

        return records
