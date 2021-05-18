from datetime import datetime
from datetime import timedelta
import pymssql

from vaccine_caregiver import VaccineCaregiver


class VaccinePatient:
    ''' Initializes adding a patient to be vaccinated. '''
    def __init__(self, PatientName, VaccineStatus, cursor):

        self.PatientName = PatientName
        self.VaccineStatus = VaccineStatus
        
        try:
            _sqlInsert = "INSERT INTO Patients (PatientName, VaccineStatus) VALUES ("
            _sqlInsert += "'" + str(PatientName) + "', '" + str(VaccineStatus) + "')" # PatientName + VaccineStatus

            cursor.execute(_sqlInsert)
            cursor.connection.commit()

            self.PatientId = 0 # similiar logic to putholdonappointmentstatus stub !!!! 

            cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            _identityRow = cursor.fetchone()
            self.PatientId = _identityRow['Identity']
            # cursor.connection.commit()
            print('Query executed successfully. Patient : ' + self.PatientName 
            +  ' added to the database using Patient ID = ' + str(self.PatientId))
            
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Vaccine Patient class!")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1]) 
                print("SQL text that resulted in an Error: " + _sqlInsert)
