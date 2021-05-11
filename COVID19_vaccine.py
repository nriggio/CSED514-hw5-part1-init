from datetime import datetime
from datetime import timedelta
import pymssql


class COVID19Vaccine:
    ''' Adds the COVID-19 Vaccine to the DB and adds/reserves doses. '''
    def __init__(self, VaccineName, cursor, PatientId = None, DosesToAdd = 0):
        
        self.VaccineName = VaccineName

        try:
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

        except NameError:
            print("Check vaccine name - only presently accepting Pfizer, Moderna, Johnson & Johnson, and Astra-Zeneca doses.")

    def AddDoses(self, VaccineName, cursor, DosesToAdd):
        ''' Adds doses to the vaccine inventory for a particular vaccine. '''
        self.VaccineName = VaccineName
        self.DosesToAdd = DosesToAdd

        if isinstance(DosesToAdd, int): # if integer (didn't restrict for negatives by choice)
            try:
                _sqltext = ("UPDATE Vaccines SET DosesAvailable = (DosesAvailable + ")
                _sqltext += str(DosesToAdd) + ") WHERE VaccineName = " + "'" + str(VaccineName) + "'"
                
                cursor.execute(_sqltext)
                cursor.connection.commit()

            except pymssql.Error as db_err:
                print("Database Programming Error in SQL Query processing for COVID-19 Vaccine doses!")
                print("Exception code: " + str(db_err.args[0]))
                if len(db_err.args) > 1:
                    print("Exception message: " + db_err.args[1]) 
                    print("SQL text that resulted in an Error: " + _sqltext)
        else:
            print('Number of doses added must be an integer.') # need error/test for this ???

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
            _sqltext1 = ("SELECT DosesAvailable FROM Vaccines WHERE VaccineName = ") + "'" + str(VaccineName) + "'"
            cursor.execute(_sqltext1)
            rows = cursor.fetchall()

            if rows[0].get('DosesAvailable') >= DosesToReserve:

                _sqltext2 = ("UPDATE Vaccines SET DosesReserved = (DosesReserved + ")
                _sqltext2 += str(DosesToReserve) + ") WHERE VaccineName = " + "'" + str(VaccineName) + "'"

                cursor.execute(_sqltext2)
                cursor.connection.commit()

                _sqltext3 = ("UPDATE Vaccines SET DosesAvailable = (DosesAvailable - ")
                _sqltext3 += str(DosesToReserve) + ") WHERE VaccineName = " + "'" + str(VaccineName) + "'"

                cursor.execute(_sqltext3)
                cursor.connection.commit()

            else:
                print('Not enough doses, can\'t reserve!')

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for COVID-19 Vaccine doses!")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1]) 
                print("SQL text that resulted in an Error: " + _sqltext)

