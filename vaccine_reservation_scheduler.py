import datetime
from enum import IntEnum
import os
import pymssql
import traceback

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from COVID19_vaccine import COVID19Vaccine as covid
# from vaccine_patient import VaccinePatient as patient


class VaccineReservationScheduler:

    def __init__(self):
        return

    def PutHoldOnAppointmentSlot(self, cursor):
        ''' Method that reserves a CareGiver appointment slot &
        returns the unique scheduling slotid
        Should return 0 if no slot is available  or -1 if there is a database error'''
        # Note to students: this is a stub that needs to replaced with your code
        self.slotSchedulingId = 0
        self.getAppointmentSQL = "SELECT SlotStatus, CaregiverSlotSchedulingId FROM CareGiverSchedule WHERE SlotStatus = 0"
        
        try:
            cursor.execute(self.getAppointmentSQL)
            rows = cursor.fetchone()
            print(rows)
            self.slotSchedulingId = rows.get('CaregiverSlotSchedulingId')

            if rows:
                _sqlUpdate = "UPDATE CareGiverSchedule SET SlotStatus = 1 WHERE CaregiverSlotSchedulingId = "
                _sqlUpdate += str(self.slotSchedulingId) # return slotSchedulingId if available

                cursor.execute(_sqlUpdate)
                cursor.connection.commit()

            return self.slotSchedulingId # return 0 if not available
        
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])           
            print("SQL text that resulted in an Error: " + self.getAppointmentSQL)
            cursor.connection.rollback()
            return -1 # return -1 if db error

    def ScheduleAppointmentSlot(self, slotid, cursor):
        '''method that marks a slot on Hold with a definite reservation  
        slotid is the slot that is currently on Hold and whose status will be updated 
        returns the same slotid when the database update succeeds 
        returns 0 is there if the database update dails 
        returns -1 the same slotid when the database command fails
        returns 21 if the slotid parm is invalid '''
        # Note to students: this is a stub that needs to replaced with your code
        if slotid < 1:
            return -2
        self.slotSchedulingId = slotid
        self.getAppointmentSQL = "SELECT something... "
        try:
            cursor.execute(self.getAppointmentSQL)
            return self.slotSchedulingId
        except pymssql.Error as db_err:    
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + db_err.args[0])
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))  
            print("SQL text that resulted in an Error: " + self.getAppointmentSQL)
            return -1

if __name__ == '__main__':
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            clear_tables(sqlClient)
            vrs = VaccineReservationScheduler()

            # get a cursor from the SQL connection
            dbcursor = sqlClient.cursor(as_dict=True) # think about using multiple cursor instances here !!!!! 

            # Iniialize the caregivers, patients & vaccine supply
            caregiversList = []
            caregiversList.append(VaccineCaregiver('Carrie Nation', dbcursor)) # allocates at least 2 caregivers
            caregiversList.append(VaccineCaregiver('Clare Barton', dbcursor))
            caregivers = {}
            for cg in caregiversList:
                cgid = cg.caregiverId
                caregivers[cgid] = cg

            # Add a vaccine and Add doses to inventory of the vaccine
            vax = covid(VaccineName = 'Pfizer', cursor = dbcursor) # adds at least 5 doses of a two-dose vaccine
            vax.AddDoses(DosesToAdd = 5, cursor = dbcursor)

            # Assign patients
            ###### ADD PATIENT FROM vaccine_patient ######

            # Schedule the patients
            ###### check PutHoldOnAppointmentSlot ######
            
            # Test cases done!
            clear_tables(sqlClient)
