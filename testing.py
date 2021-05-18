# imports
import unittest
import os

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from covid19_vaccine import COVID19Vaccine as covid


# test string concatenation
VaccineName = 'Pfizer'
DosesToAdd = 100
_sqlCHECK = ("SELECT * FROM Vaccines WHERE '")
_sqlCHECK += str(VaccineName) + "'"
print(_sqlCHECK)

_sqltext = ("UPDATE Vaccines SET AvailableDoses = (AvailableDoses + ")
_sqltext += str(DosesToAdd) + ") WHERE " + "'" + str(VaccineName) + "'"
print(_sqltext)

_VaccineName = 'Pfizer'
_VaccineSupplier = 'Pfizer'
_MaxStorageTemp = '10 F'
_DosesPerPatient = 2
_DaysBetweenDoses = 21

_sqlInsert = "INSERT INTO Vaccines (VaccineName, VaccineSupplier, MaxStorageTemp, DosesPerPatient, DaysBetweenDoses) VALUES ("
_sqlInsert += "'" + str(_VaccineName) + "', '" + str(_VaccineSupplier) + "', '" + str(_MaxStorageTemp) + "', '" # Vaccine Name + Supplier + Temp
_sqlInsert += str(_DosesPerPatient) + ", " + str(_DaysBetweenDoses) + ")" # Doses + Spacing
print(_sqlInsert)


import unittest
import os

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from COVID19_vaccine import COVID19Vaccine as covid


with SqlConnectionManager(Server=os.getenv("Server"),
                            DBname=os.getenv("DBName"),
                            UserId=os.getenv("UserID"),
                            Password=os.getenv("Password")) as sqlClient:
    with sqlClient.cursor(as_dict=True) as cursor:           
        # Add multiple doses to vaccines
        covid = covid(VaccineName = 'Pfizer', cursor = cursor).AddDoses(DosesToAdd = 100, cursor = cursor)
        covid.AddDoses(DosesToAdd = 50, cursor = cursor)

        # check if the vaccine is correctly inserted into the database
        sqlQuery = '''
                    SELECT AvailableDoses
                    FROM Vaccines
                    WHERE VaccineName = 'Pfizer'
                    ''' 
                    
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        print(rows)

