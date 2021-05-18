from datetime import datetime
from datetime import timedelta
import pymssql


class COVID19Vaccine:
    ''' Adds the COVID-19 Vaccine to the DB and adds/reserves doses. '''
    def __init__(self, VaccineName, cursor): #, PatientId = None, DosesToAdd = 0):
        
        self.VaccineName = VaccineName

        try:
            if VaccineName == 'Pfizer':
                _VaccineName = 'Pfizer'
                _VaccineSupplier = 'Pfizer'
                _MaxStorageTemp = '-75 F'
                _DosesPerPatient = 2
                _DaysBetweenDoses = 21

            elif VaccineName == 'Moderna':
                _VaccineName = 'Moderna'
                _VaccineSupplier = 'Moderna'
                _MaxStorageTemp = '-75 F'
                _DosesPerPatient = 2
                _DaysBetweenDoses = 28

            elif VaccineName == 'Johnson & Johnson':
                _VaccineName = 'Johnson & Johnson'
                _VaccineSupplier = 'Johnson & Johnson'
                _MaxStorageTemp = '46 F'
                _DosesPerPatient = 1
                _DaysBetweenDoses = 0

            elif VaccineName == 'Astra-Zeneca':
                _VaccineName = 'Astra-Zeneca'
                _VaccineSupplier = 'Astra-Zeneca'
                _MaxStorageTemp = '46 F'
                _DosesPerPatient = 2
                _DaysBetweenDoses = 56

            _sqlInsert = "INSERT INTO Vaccines (VaccineName, VaccineSupplier, MaxStorageTemp, DosesPerPatient, DaysBetweenDoses) VALUES ("
            _sqlInsert += "'" + str(_VaccineName) + "', '" + str(_VaccineSupplier) + "', '" + str(_MaxStorageTemp) + "', " # Vaccine Name + Supplier + Temp
            _sqlInsert += str(_DosesPerPatient) + ", " + str(_DaysBetweenDoses) + ")" # Doses + Spacing

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
                print("SQL text that resulted in an Error: " + _sqlInsert)

        except NameError:
            print("Check vaccine name - only presently accepting Pfizer, Moderna, Johnson & Johnson, and Astra-Zeneca doses.")

    def AddDoses(self, DosesToAdd, cursor): 
        ''' Adds doses to the vaccine inventory for a particular vaccine. '''

        if isinstance(DosesToAdd, int) == True and DosesToAdd >= 0: # if positive integer!!!!
            try:
                self._sqlUpdate = "UPDATE Vaccines SET AvailableDoses = (AvailableDoses + "
                self._sqlUpdate += str(DosesToAdd) + "), TotalDoses = (TotalDoses + "
                self._sqlUpdate += str(DosesToAdd) + ") WHERE VaccineName = " + "'" + str(self.VaccineName) + "'"
                # self._sqlUpdate = "UPDATE Vaccines SET AvailableDoses = (AvailableDoses + {}), TotalDoses = (TotalDoses + {}) WHERE VaccineName = {}".format(DosesToAdd, DosesToAdd, "'" + self.VaccineName + "'")
                # print("query to execute: ", self._sqlUpdate)

                cursor.execute(self._sqlUpdate)
                cursor.connection.commit()

            except pymssql.Error as db_err:
                print("Database Programming Error in SQL Query processing for COVID-19 Vaccine doses!")
                print("Exception code: " + str(db_err.args[0]))
                if len(db_err.args) > 1:
                    print("Exception message: " + db_err.args[1]) 
                    print("SQL text that resulted in an Error: " + self._sqlUpdate)
        else:
            print('Number of doses added must be a positive integer.') # need error/test for this ???

    def ReserveDoses(self, cursor): # not tying to patient yet
    # def ReserveDoses(self, VaccineName, cursor, PatientId):
        ''' Reserves doses associated with a specific patient who is being scheduled for vaccine administration. '''
        ''' Just shows doses as reserved for now, handle DosesPerPatient to reserve both @ same time, don't reserve any if not enough. '''

        doses2 = ['Pfizer', 'Moderna']
        doses1 = ['Johnson & Johnson', 'Astra-Zeneca']

        if self.VaccineName in doses2:
            DosesToReserve = 2
        elif self.VaccineName in doses1:
            DosesToReserve = 1 

        try:
            self._sqlCheck = "SELECT AvailableDoses FROM Vaccines WHERE VaccineName = " + "'" + str(self.VaccineName) + "'"
            cursor.execute(self._sqlCheck)
            rows = cursor.fetchall()

            if rows[0].get('AvailableDoses') >= DosesToReserve: 

                self._sqlUpdate = "UPDATE Vaccines SET ReservedDoses = (ReservedDoses + "
                self._sqlUpdate += str(DosesToReserve) + "), AvailableDoses = (AvailableDoses - "
                self._sqlUpdate += str(DosesToReserve) + ") WHERE VaccineName = " + "'" + str(self.VaccineName) + "'"

                cursor.execute(self._sqlUpdate)
                cursor.connection.commit()

            else:
                print('Not enough doses, can\'t reserve!')

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for COVID-19 Vaccine doses!")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1]) 
                print("SQL text that resulted in an Error: " + self._sqlUpdate)

