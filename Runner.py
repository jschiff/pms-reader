import io
import sys
from PMSReader import PMSReader


def main():
    reader = PMSReader()
    with io.open(sys.argv[1], 'rb') as patients_file:
        patient_records = reader.read_patient_record_stream(patients_file)

    print_patient_records(patient_records)
    check_for_unique_ids(patient_records)
    print (len(patient_records))


def print_patient_records(patient_records):
    for record in patient_records:
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
