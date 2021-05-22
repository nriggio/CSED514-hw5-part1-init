import unittest
import os

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from COVID19_vaccine import COVID19Vaccine as covid
from vaccine_patient import VaccinePatient as patient

class TestDB(unittest.TestCase):

    def test_db_connection(self):
        try:
            self.connection_manager = SqlConnectionManager(Server=os.getenv("Server"),
                                                           DBname=os.getenv("DBName"),
                                                           UserId=os.getenv("UserID"),
                                                           Password=os.getenv("Password"))
            self.conn = self.connection_manager.Connect()
        except Exception:
            self.fail("Connection to database failed")


class TestVaccinePatient(unittest.TestCase):
    def test_patient_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # create a new Patient object
                    self.vaccinepatient = patient(PatientName = "Nicole Riggio", VaccineStatus = 0, cursor = cursor)

                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT *
                               FROM Patients
                               WHERE PatientName = 'Nicole Riggio'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if len(rows) != 1: 
                        self.fail("Creating patient failed")

                    elif len(rows) == 1:
                        print('Patient was added initialized in Patients!')

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)

                    self.fail("Creating patient failed due to exception")

    # def test_reserveappointment(self):
    #     with SqlConnectionManager(Server=os.getenv("Server"),
    #                               DBname=os.getenv("DBName"),
    #                               UserId=os.getenv("UserID"),
    #                               Password=os.getenv("Password")) as sqlClient:
    #         with sqlClient.cursor(as_dict=True) as cursor:
    #             try:
    #                 # clear the tables before testing
    #                 clear_tables(sqlClient)

    #                 # create a new Patient object
    #                 self.vaccineappt = patient(PatientName = "Nicole Riggio", VaccineStatus = 1, cursor = cursor)
    #                 # self.vaccineappt.ReserveAppointment(CaregiverSchedulingID = , Vaccine = 'Pfizer', cursor = cursor)

    #                 # check if the patient is correctly inserted into the database
    #                 sqlQuery = '''
    #                            SELECT *
    #                            FROM Patients
    #                            WHERE PatientName = 'Nicole Riggio'
    #                            '''
    #                 cursor.execute(sqlQuery)
    #                 rows = cursor.fetchall()

    #                 if len(rows) != 1: 
    #                     self.fail("Creating patient failed")

    #                 elif len(rows) == 1:
    #                     print('Patient was added initialized in Patients!')

    #                 # clear the tables after testing, just in-case
    #                 clear_tables(sqlClient)

    #             except Exception:
    #                 # clear the tables if an exception occurred
    #                 clear_tables(sqlClient)

    #                 self.fail("Creating patient failed due to exception")


if __name__ == '__main__':
    unittest.main()