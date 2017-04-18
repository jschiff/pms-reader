import io
import sys
from PMSReader import PMSReader

def print_patient_records(patient_records):
    for record in patient_records:
        print(record)

def check_for_unique_ids(patient_records):
    uniqueIds = {}
    foundDuplicate = False
    recordcount = 0
    for record in patient_records:
        if uniqueIds.get(record.id, False):
            foundDuplicate = True
        else:
            uniqueIds[record.id] = recordcount
        recordcount += 1

    print ('Found' if foundDuplicate else 'Did not find') + ' duplicate ids in the records'

reader = PMSReader()
with io.open(sys.argv[1], 'rb') as patients_file:
    patientRecords = reader.read_patient_record_stream(patients_file)

print_patient_records(patientRecords)
check_for_unique_ids(patientRecords)
print (len(patientRecords))
