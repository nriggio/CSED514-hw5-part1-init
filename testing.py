#test
VaccineName = 'Pfizer'
_sqlCHECK = ("SELECT * FROM Vaccines WHERE '")
_sqlCHECK += str(VaccineName) + "'"
print(_sqlCHECK)
