from datetime import datetime
from datetime import timedelta
import pymssql


class COVID19Vaccine:
    ''' Adds the COVID-19 Vaccine to the DB and adds/reserves doses. '''
    def __init__(self, VaccineName, cursor):

        try:
            self.VaccineName = VaccineName

            # # does this need provision for if VaccineName already exists do NOT add again????
            # # check if VaccineName already exists
            # _sqlCHECK = ("SELECT * FROM Vaccines WHERE '")
            # _sqlCHECK += str(VaccineName) + "'")
            # cursor.execute(sqlQuery)
            # rows = cursor.fetchall()

            # if len(rows) == 1:
            #     print('Can\'t add because already exists, try AddDoses or ReserveDoses instead.')

            # elif len(rows) == 0: ### change indents below if used

            if VaccineName == 'Pfizer':
                _DosesRequired = 2
                _MaxSpacing = 42
                _MinSpacing = 21

                _sqltext = ("INSERT INTO Vaccines (VaccineName, DosesRequired, MaxSpacing, MinSpacing, MaxStorageTemp) VALUES (") 
                _sqltext += str("'Pfizer'") + ", " # VaccineName
                _sqltext += str(_DosesRequired) + ", " + str(_MaxSpacing) + ", " + str(_MinSpacing) + ", " # Doses + Spacing
                _sqltext += str("'-75 F'") + ")" # MaxStorageTemp

            elif VaccineName == 'Moderna':
                _DosesRequired = 2
                _MaxSpacing = 42
                _MinSpacing = 28

                _sqltext = ("INSERT INTO Vaccines (VaccineName, DosesRequired, MaxSpacing, MinSpacing, MaxStorageTemp) VALUES (") 
                _sqltext += str("'Moderna'") + ", " # VaccineName
                _sqltext += str(_DosesRequired) + ", " + str(_MaxSpacing) + ", " + str(_MinSpacing) + ", " # Doses + Spacing
                _sqltext += str("'-75 F'") + ")" # MaxStorageTemp

            elif VaccineName == 'Johnson & Johnson':
                _DosesRequired = 1
                _MaxSpacing = 0
                _MinSpacing = 0

                _sqltext = ("INSERT INTO Vaccines (VaccineName, DosesRequired, MaxSpacing, MinSpacing, MaxStorageTemp) VALUES (") 
                _sqltext += str("'Johnson & Johnson'") + ", " # VaccineName
                _sqltext += str(_DosesRequired) + ", " + str(_MaxSpacing) + ", " + str(_MinSpacing) + ", " # Doses + Spacing
                _sqltext += str("'46 F'") + ")" # MaxStorageTemp

            elif VaccineName == 'Astra-Zeneca':
                _DosesRequired = 2
                _MaxSpacing = 84
                _MinSpacing = 56

                _sqltext = ("INSERT INTO Vaccines (VaccineName, DosesRequired, MaxSpacing, MinSpacing, MaxStorageTemp) VALUES (") 
                _sqltext += str("'Astra-Zeneca'") + ", " # VaccineName
                _sqltext += str(_DosesRequired) + ", " + str(_MaxSpacing) + ", " + str(_MinSpacing) + ", " # Doses + Spacing
                _sqltext += str("'46 F'") + ")" # MaxStorageTemp

            cursor.execute(_sqltext)
            cursor.connection.commit()

            cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            _identityRow = cursor.fetchone()
            self.VaccineId = _identityRow['Identity']
            # cursor.connection.commit()
            print('Query executed successfully. Vaccine : ' + self.VaccineName 
            +  ' added to the database using Vaccine ID = ' + str(self.VaccineId))
            
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for COVID-19 Vaccine doses!")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1]) 
                print("SQL text that resulted in an Error: " + _sqltext)

        # except NameError:
        #     print("Check vaccine name - only presently accepting Pfizer, Moderna, Johnson & Johnson, and Astra-Zeneca doses.")

    def AddDoses(self, VaccineName, DosesToAdd, cursor):
        ''' Adds doses to the vaccine inventory for a particular vaccine. '''
        try:
            self.VaccineName = VaccineName
            self.DosesToAdd = _DosesToAdd
            _sqltext = ("UPDATE Vaccines SET TotalDoses = TotalDoses + ")
            _sqltext += _DosesToAdd + "WHERE" + "'" + str(VaccineName) + "'"
            
            cursor.execute(_sqltext)
            cursor.connection.commit()

            cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            _identityRow = cursor.fetchone()
            self.VaccineId = _identityRow['Identity']
            # cursor.connection.commit()
            print('Query executed successfully. Doses: ' + self.DosesToAdd
            + 'of ' + self.VaccineName 
            +  ' added to the database using Vaccine ID = ' + str(self.VaccineId))

        # need exception for non-integer values ????

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for COVID-19 Vaccine doses!")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1]) 
                print("SQL text that resulted in an Error: " + _sqltext)

    def ReserveDoses(self, DosesToReserve, cursor):
        ''' Reserves doses associated with a specific patient who is being scheduled for vaccine administration. '''
        pass

