import io
import sys
from PMSReader import PMSReader


def main():
    reader = PMSReader()
    if len(sys.argv) < 3:
        print 'Usage: python Runner.py mode file\n' \
              '    modes: d - dentist mode, p - patient mode'
        exit(1)

    with io.open(sys.argv[2], 'rb') as data_file:
        if sys.argv[1] == 'd':
            records = reader.read_provider_record_stream(data_file)
        else:
            records = reader.read_patient_record_stream(data_file)

    print_records(records)
    check_for_unique_ids(records)
    print (len(records))


def print_records(records):
    for record in records:
        print(record)


def check_for_unique_ids(patient_records):
    unique_ids = {}
    found_duplicate = False
    record_count = 0
    for record in patient_records:
        if unique_ids.get(record.id, False):
            found_duplicate = True
        else:
            unique_ids[record.id] = record_count
        record_count += 1

    print ('Found' if found_duplicate else 'Did not find') + ' duplicate ids in the records'

main()
