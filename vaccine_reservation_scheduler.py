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
from vaccine_patient import VaccinePatient as patient
# import vaccine_patient as patient # watch for circular imports ????


class VaccineReservationScheduler:

    def __init__(self):
        return

    def PutHoldOnAppointmentSlot(self, cursor): #CaregiverSchedulingID, cursor):
        ''' Method that reserves a CareGiver appointment slot &
        returns the unique scheduling slotid
        Should return 0 / -2 if no slot is available  or -1 if there is a database error'''
        # Note to students: this is a stub that needs to replaced with your code
        self.slotSchedulingId = 0 # change to -2 per Lab discussion (0 = acceptable value !) ????
        self.getAppointmentSQL = "SELECT SlotStatus, CaregiverSlotSchedulingId FROM CareGiverSchedule WHERE SlotStatus = 0"
        
        try:
            cursor.execute(self.getAppointmentSQL)
            rows = cursor.fetchone() 
            self.slotSchedulingId = rows.get('CaregiverSlotSchedulingId')

            if rows: # if have an open slot, change slotstatus to "on hold"
                _sqlUpdate = "UPDATE CareGiverSchedule SET SlotStatus = 1 WHERE CaregiverSlotSchedulingId = "+  str(self.slotSchedulingId)

                cursor.execute(_sqlUpdate)
                cursor.connection.commit()

            else:
                print('No Open slots to put On Hold')

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
        returns -2 if the slotid parm is invalid '''
        # Note to students: this is a stub that needs to replaced with your code
        if slotid < 0:
            return -2
        self.slotSchedulingId = slotid
        self.getAppointmentSQL = "SELECT SlotStatus FROM CareGiverSchedule WHERE SlotStatus = 1 AND CaregiverSlotSchedulingId = " + str(self.slotSchedulingId)

        try:
            cursor.execute(self.getAppointmentSQL)
            rows = cursor.fetchone()
            self.slotSchedulingId = rows.get('CaregiverSlotSchedulingId')

            if rows:
                self.slotSchedulingId = slotid
                _sqlUpdate = "UPDATE CareGiverSchedule SET SlotStatus = 2 WHERE CaregiverSlotSchedulingId = "+  str(self.slotSchedulingId)

                cursor.execute(_sqlUpdate)
                cursor.connection.commit()

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

            vrs = VaccineReservationScheduler() # use to call PutHoldOnAppointmentSlot

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

            # patient 1
            new_patient = patient(PatientName = 'Nicole Riggio', VaccineStatus = 0, VaccineName = 'Pfizer', cursor = dbcursor)
            p1d1 = new_patient.ReserveAppointment(CaregiverSchedulingID = vrs.PutHoldOnAppointmentSlot(cursor = dbcursor), cursor = dbcursor)
            new_patient.ScheduleAppointment(CaregiverSchedulingID = vrs.ScheduleAppointmentSlot(slotid = p1d1, cursor = dbcursor), cursor = dbcursor)

            # patient 2
            new_patient2 = patient(PatientName = 'Alyson Suchodolski', VaccineStatus = 0, VaccineName = 'Pfizer', cursor = dbcursor)
            p2d1 = new_patient2.ReserveAppointment(CaregiverSchedulingID = vrs.PutHoldOnAppointmentSlot(cursor = dbcursor), cursor = dbcursor)
            new_patient2.ScheduleAppointment(CaregiverSchedulingID = vrs.ScheduleAppointmentSlot(slotid = p2d1, cursor = dbcursor), cursor = dbcursor)

            # patient 3
            new_patient3 = patient(PatientName = 'John Doe', VaccineStatus = 0, VaccineName = 'Pfizer', cursor = dbcursor)
            p3d1 = new_patient3.ReserveAppointment(CaregiverSchedulingID = vrs.PutHoldOnAppointmentSlot(cursor = dbcursor), cursor = dbcursor)
            new_patient3.ScheduleAppointment(CaregiverSchedulingID = vrs.ScheduleAppointmentSlot(slotid = p3d1, cursor = dbcursor), cursor = dbcursor)
            
            # Test cases done!
            clear_tables(sqlClient)
