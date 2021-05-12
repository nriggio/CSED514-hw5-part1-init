from datetime import datetime
from datetime import timedelta
import pymssql


class COVID19Vaccine:
    ''' Adds the COVID-19 Vaccine to the DB and adds/reserves doses. '''
    def __init__(self, VaccineName, cursor, PatientId = None, DosesToAdd = 0):
        
        self.VaccineName = VaccineName

        try:
            if VaccineName == 'Pfizer':
                _VaccineName = 'Pfizer'
                _DosesRequired = 2
                _MaxSpacing = 42
                _MinSpacing = 21
                _MaxStorageTemp = '-75 F'

            elif VaccineName == 'Moderna':
                _VaccineName = 'Moderna'
                _DosesRequired = 2
                _MaxSpacing = 42
                _MinSpacing = 28
                _MaxStorageTemp = '-75 F'

            elif VaccineName == 'Johnson & Johnson':
                _VaccineName = 'Johnson & Johnson'
                _DosesRequired = 1
                _MaxSpacing = 0
                _MinSpacing = 0
                _MaxStorageTemp = '46 F'

            elif VaccineName == 'Astra-Zeneca':
                _VaccineName = 'Astra-Zeneca'
                _DosesRequired = 2
                _MaxSpacing = 84
                _MinSpacing = 56
                _MaxStorageTemp = '46 F'

            _sqlInsert = ("INSERT INTO Vaccines (VaccineName, DosesRequired, MaxSpacing, MinSpacing, MaxStorageTemp) VALUES (") 
            _sqlInsert += "'" + str(_VaccineName) + "', " # VaccineName
            _sqlInsert += str(_DosesRequired) + ", " + str(_MaxSpacing) + ", " + str(_MinSpacing) + ", " # Doses + Spacing
            _sqlInsert += "'" + str(_MaxStorageTemp) + "')" # MaxStorageTemp

            cursor.execute(_sqlInsert)
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

        except NameError:
            print("Check vaccine name - only presently accepting Pfizer, Moderna, Johnson & Johnson, and Astra-Zeneca doses.")

    def AddDoses(self, VaccineName, cursor, DosesToAdd):
        ''' Adds doses to the vaccine inventory for a particular vaccine. '''
        self.VaccineName = VaccineName
        self.DosesToAdd = DosesToAdd

        # fix !!!!
        # if isinstance(float(DosesToAdd), int) == True and float(DosesToAdd) >= 0: # if positive integer!!!!
        try:
            _sqlUpdate = ("UPDATE Vaccines SET DosesAvailable = (DosesAvailable + ")
            _sqlUpdate += str(DosesToAdd) + ") WHERE VaccineName = " + "'" + str(VaccineName) + "'"
            
            cursor.execute(_sqlUpdate)
            cursor.connection.commit()

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for COVID-19 Vaccine doses!")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1]) 
                print("SQL text that resulted in an Error: " + _sqltext)
        # else:
        #     print('Number of doses added must be a positive integer.') # need error/test for this ???

    def ReserveDoses(self, VaccineName, cursor): # not tying to patient yet
    # def ReserveDoses(self, VaccineName, cursor, PatientId):
        ''' Reserves doses associated with a specific patient who is being scheduled for vaccine administration. '''
        ''' Just shows doses as reserved for now, handle DosesRequired to reserve both @ same time, don't reserve any if not enough. '''
        self.VaccineName = VaccineName
        # self.PatientId = PatientId

        doses2 = ['Pfizer', 'Moderna']
        doses1 = ['Johnson & Johnson', 'Astra-Zeneca']

        if VaccineName in doses2:
            DosesToReserve = 2
        elif VaccineName in doses1:
            DosesToReserve = 1 

        try:
            _sqlCheck = ("SELECT DosesAvailable FROM Vaccines WHERE VaccineName = ") + "'" + str(VaccineName) + "'"
            cursor.execute(_sqlCheck)
            rows = cursor.fetchall()

            if rows[0].get('DosesAvailable') >= DosesToReserve: 

                _sqlUpdate = ("UPDATE Vaccines SET DosesReserved = (DosesReserved + ")
                _sqlUpdate += str(DosesToReserve) + "), DosesAvailable = (DosesAvailable - "
                _sqlUpdate += str(DosesToReserve) + ") WHERE VaccineName = " + "'" + str(VaccineName) + "'"

                cursor.execute(_sqlUpdate)
                cursor.connection.commit()

            else:
                print('Not enough doses, can\'t reserve!')

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for COVID-19 Vaccine doses!")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1]) 
                print("SQL text that resulted in an Error: " + _sqltext)

