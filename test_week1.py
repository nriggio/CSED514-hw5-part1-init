import unittest
import os

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from covid19_vaccine import COVID19Vaccine as covid
# from vaccine_patient import VaccinePatient as patient

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


class TestCOVID19Vaccine(unittest.TestCase):
    def test_vaccine_addition(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new Vaccine object
                    self.covid19vaccine_a = covid(VaccineName = "Johnson & Johnson",
                                                    cursor=cursor)
                    # check if the vaccine is correctly inserted into the database
                    sqlQuery = '''
                               SELECT *
                               FROM Vaccines
                               WHERE VaccineName = 'Johnson & Johnson'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if len(rows) != 1: # not equal to one (only 1 row per VaccineName)
                        self.fail("Creating vaccine failed")
                        clear_tables(sqlClient)

                    elif len(rows) == 1:
                        clear_tables(sqlClient)
                        print('Vaccine was added successfully to Vaccines.')

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Creating vaccine failed due to exception")
    
    def test_bad_vaccine_name(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new Vaccine object
                    self.covid19vaccine_a = covid(VaccineName = "Janssen",
                                                    cursor=cursor)
                    # check if bad vaccine name has NOT been inserted into Vaccines
                    sqlQuery = '''
                               SELECT *
                               FROM Vaccines
                               WHERE VaccineName = 'Janssen'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if len(rows) != 0: # not equal to one (only 1 row per VaccineName)
                        self.fail("Added vaccine when it should not have!")
                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    #self.fail("Some other exception, please check!")
                    print('Didn\'t add vaccine to Vaccines because it is not a supported VaccineName.')


if __name__ == '__main__':
    unittest.main()
