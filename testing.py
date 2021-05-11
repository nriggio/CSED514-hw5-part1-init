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

_sqltext = ("UPDATE Vaccines SET DosesAvailable = (DosesAvailable + ")
_sqltext += str(DosesToAdd) + ") WHERE " + "'" + str(VaccineName) + "'"
print(_sqltext)

VaccineName = 'Pfizer'
DosesToReserve = 2
_sqltext2 = ("UPDATE Vaccines SET DosesReserved = (DosesReserved + ")
_sqltext2 += str(DosesToReserve) + ") WHERE VaccineName = " + "'" + str(VaccineName) + "'"
print(_sqltext2)