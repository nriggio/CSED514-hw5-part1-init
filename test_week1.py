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


class TestCOVID19Vaccine(unittest.TestCase):
    def test_vaccine_init_good(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # create a new Vaccine object
                    self.covid = covid(VaccineName = "Johnson & Johnson", cursor = cursor)

                    # check if the vaccine is correctly inserted into the database
                    sqlQuery = '''
                               SELECT *
                               FROM Vaccines
                               WHERE VaccineName = 'Johnson & Johnson'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if len(rows) != 1: # 1 row per VaccineName
                        self.fail("Creating vaccine failed")

                    elif len(rows) == 1:
                        print('Vaccine was added initialized in Vaccines!')

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)

                    self.fail("Creating vaccine failed due to exception")
    
    def test_vaccine_init_bad(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # create a new Vaccine object
                    self.covid = covid(VaccineName = "Janssen", cursor = cursor)

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
    
    def test_AddDoses(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # Add doses to Vaccines
                    self.covid = covid(VaccineName = 'Pfizer', cursor = cursor)
                    self.covid.AddDoses(DosesToAdd = 100, cursor = cursor)

                    # check if the vaccine is correctly inserted into the database
                    sqlQuery = '''
                               SELECT AvailableDoses
                               FROM Vaccines
                               WHERE VaccineName = 'Pfizer'
                               ''' 
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if rows[0].get('AvailableDoses') == 100: # not equal to one (only 1 row per VaccineName)
                        print("The vaccine doses were added!")

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("The doses were NOT added.")

    def test_AddDoses_recursion(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    
                    # Add multiple doses to vaccines
                    self.covid = covid(VaccineName = 'Pfizer', cursor = cursor)
                    self.covid.AddDoses(DosesToAdd = 100, cursor = cursor)
                    self.covid.AddDoses(DosesToAdd = 50, cursor = cursor)

                    # check if the vaccine is correctly inserted into the database
                    sqlQuery = '''
                               SELECT AvailableDoses, TotalDoses
                               FROM Vaccines
                               WHERE VaccineName = 'Pfizer'
                               ''' 
                               
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    # print(rows)

                    if rows[0].get('TotalDoses') == 150: # not equal to one (only 1 row per VaccineName)
                        print("The vaccine doses were added recursively!")

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("The doses were NOT added.")

    def test_ReserveDoses(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # Add doses to Vaccine & reserve for 1 patient
                    self.covid = covid(VaccineName = 'Moderna', cursor = cursor) 
                    self.covid.AddDoses(DosesToAdd = 10, cursor = cursor)
                    self.covid.ReserveDoses(cursor = cursor)

                    # check if the vaccine is correctly inserted into the database
                    sqlQuery = '''
                               SELECT ReservedDoses, AvailableDoses
                               FROM Vaccines
                               WHERE VaccineName = 'Moderna'
                               ''' 
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall() 
                    # print(rows)

                    if rows[0].get('ReservedDoses') == 2 and rows[0].get('AvailableDoses') == 8: 
                        print("The vaccine doses were reserved and removed from AvailableDoses!")

                    else:
                        print('Not enough doses so (correctly) didn\'t reserve or remove from AvailableDoses!')

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("The doses were NOT reserved.")

    def test_ReserveDoses_multiple(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # Add doses to Vaccines & reserve for 2 patients
                    self.covid = covid(VaccineName = 'Moderna', cursor = cursor)
                    self.covid.AddDoses(DosesToAdd = 10, cursor = cursor)
                    self.ReserveDoses = self.covid.ReserveDoses(cursor = cursor)
                    self.ReserveDoses = self.covid.ReserveDoses(cursor = cursor)

                    # check if the vaccine is correctly inserted into the database
                    sqlQuery = '''
                               SELECT ReservedDoses, AvailableDoses
                               FROM Vaccines
                               WHERE VaccineName = 'Moderna'
                               ''' 
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall() 
                    # print(rows)

                    if rows[0].get('ReservedDoses') == 4 and rows[0].get('AvailableDoses') == 6: 
                        print("The vaccine doses were reserved for two patients!")

                    else:
                        print('Not enough doses so (correctly) didn\'t reserve or remove from AvailableDoses!')

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("The doses were NOT reserved.")


if __name__ == '__main__':
    unittest.main()
