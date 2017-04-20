# -*- coding: utf-8 -*-
from PatientRecord import PatientRecord
from StringIO import StringIO


def normalize_text(text):
    text = text.replace('\00', '').strip()
    return None if text == '' else text


def format_as_hex_string(value):
    return ''.join(x.encode('hex') for x in value)


class PMSReader:
    section_lengths = [
        # Record ID
        16,
        14,
        # First name
        16,
        # Middle name
        16,
        # Last name
        16,
        16,
        82,
        11,
        # Phone number
        20,
        # Also a phone number
        19,
        # Sometimes contains full name
        36,
        # ID that contains gender information
        12,
        104,
        7,
        624,
        370,
        36,
        593
    ]

    PADDING_SECTION_A = '\xff' * section_lengths[0]

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

        # Ignore the header and initial padding by skipping one section length of data.
        raw_data.read(sum(PMSReader.section_lengths))

        section_data = [None] * len(PMSReader.section_lengths)
        section_data[0] = raw_data.read(PMSReader.section_lengths[0])
        while section_data[0] != '' and section_data[0] != PMSReader.PADDING_SECTION_A:
            record = PatientRecord()
            for i in range(1, len(PMSReader.section_lengths)):
                section_data[i] = (raw_data.read(PMSReader.section_lengths[i]))

            # Save the data we care about.
            record.id = format_as_hex_string(section_data[0])
            record.firstName = normalize_text(section_data[2])
            record.lastName = normalize_text(section_data[4])
            record.phone1 = normalize_text(section_data[8])
            record.phone2 = normalize_text(section_data[9])
            record.gender = normalize_text(section_data[11])
            record.gender = None if not record.gender else record.gender[0]

            records.append(record)

            # Prime for the next iteration
            section_data = [None] * len(PMSReader.section_lengths)
            section_data[0] = raw_data.read(PMSReader.section_lengths[0])

        return records
