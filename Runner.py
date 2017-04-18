import io
from PMSReader import PMSReader

def printPatientRecords(patientRecords):
    for record in patientRecords:
        print(record)

def checkForUniqueIds(patientRecords):
    uniqueIds = {}
    foundDuplicate = False
    recordcount = 0
    for record in patientRecords:
        if uniqueIds.get(record.id, False):
            foundDuplicate = True
            # print "Found duplicate value {0} from record {1} at record {2}".format(record.id, str(uniqueIds[record.id]), str(recordcount))
        else:
            uniqueIds[record.id] = recordcount
        recordcount += 1

    print ('Found' if foundDuplicate else 'Did not find') + ' duplicate ids in the records'

reader = PMSReader()
with io.open('/Users/jschiff/nexhealth/data/patient.dat', 'rb') as patientsFile:
    patientRecords = reader.readPatientRecordStream(patientsFile)

printPatientRecords(patientRecords)
checkForUniqueIds(patientRecords)
print (len(patientRecords))
