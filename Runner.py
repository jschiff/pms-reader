import io
from PMSReader import PMSReader

with io.open('/Users/jschiff/nexhealth/data/patient.dat', 'rb') as patientsFile:
    reader = PMSReader()
    reader.readPatientRecordStream(patientsFile)
