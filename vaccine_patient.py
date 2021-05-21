from datetime import datetime
from datetime import timedelta
import pymssql

from vaccine_caregiver import VaccineCaregiver
from COVID19_vaccine import COVID19Vaccine as covid
# from vaccine_patient import VaccinePatient as patient
# from vaccine_reservation_scheduler import VaccineReservationScheduler


class VaccinePatient:
    ''' Initializes adding a patient to be vaccinated. '''
    def __init__(self, PatientName, VaccineStatus, cursor):

        self.PatientName = PatientName
        self.VaccineStatus = VaccineStatus
    
        # self.PatientId = 0 # similiar logic to putholdonappointmentstatus stub !!!! 
        
        try:
            _sqlInsert = "INSERT INTO Patients (PatientName, VaccineStatus) VALUES ("
            _sqlInsert += "'" + str(PatientName) + "', " + str(VaccineStatus) + ")" # PatientName + VaccineStatus
            # print('Patient insert query: ', _sqlInsert)

            cursor.execute(_sqlInsert)
            cursor.connection.commit()

            cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            _identityRow = cursor.fetchone()
            self.PatientId = _identityRow['Identity']
            cursor.connection.commit() # needed ???
            print('Query executed successfully. Patient : ' + self.PatientName 
            +  ' added to the database using Patient ID = ' + str(self.PatientId))
            
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Vaccine Patient class!")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1]) 
                print("SQL text that resulted in an Error: " + _sqlInsert)

    def ReserveAppointment(self, CaregiverSchedulingID, Vaccine, cursor):
        ''' Method to verify if CaregiverSchedulingID = OnHold,
        create initial entry in VaccineAppointment table,
        flag Patient as "queued for dose 1", & create 2nd appointment. 
        * BE SURE TO RETAIN CLASS INSTANCE VARIABLES (i.e. Identity vals from 2 VaccineAppointment slots). '''
        ''' query CaregiverSchedule to get slotId, mark it "on hold" (via PutHoldOnAppointmentSlot()) '''

        self.Vaccine = Vaccine
        self.CaregiverSchedulingID = CaregiverSchedulingID

        try:
            # 1st: verify that CaregiverSlotSchedulingId passed is "On Hold"
            _sqlCheckApptStatus = "SELECT * FROM CareGiverSchedule WHERE CaregiverSlotSchedulingId = " + str(CaregiverSchedulingID)
            # print('ReserveAppointments check query: ', _sqlCheckApptStatus)

            cursor.execute(_sqlCheckApptStatus)
            appt_row = cursor.fetchone() # should only have 1 row per CaregiverSlotSchedulingId
            # print('appt_row', appt_row)
            
            _CaregiverId = appt_row.get('CaregiverId')
            _ReservationDate = appt_row.get('WorkDay')
            _ReservationStartHour = appt_row.get('SlotHour')
            _ReservationStartMinute = appt_row.get('SlotMinute')
            _SlotStatus = appt_row.get('SlotStatus')
            _AppointmentDuration = 15

            if _SlotStatus != 1: # if SlotStatus not = "On Hold"
                print("This slot is not available to reserve (please place OnHold)!")
                raise Exception

            # 2nd: get patient details
            _sqlCheckPatientStatus = "SELECT * FROM Patients WHERE PatientName = '" + str(self.PatientName) + "'" # check if right call
            # print('Patient check query: ', _sqlCheckPatientStatus)

            cursor.execute(_sqlCheckPatientStatus)
            patient_row = cursor.fetchone()
            # print('patient_row', patient_row)

            _VaccineStatus = patient_row.get('VaccineStatus')

            # check if eligible for 1st dose scheduling
            if _VaccineStatus == 0: # NEED TO CHECK IF TWO DOSES REQUIRED !!!!!
                # queue for 1st dose & update patient / vaccine appointment status
                _UpdatedVaccineStatus = 1 # "queued for 1st dose"
                _DoseNumber = 1

                # create appointment
                _sqlInsertAppt = "INSERT INTO VaccineAppointments (VaccineName, PatientId, CaregiverId, ReservationDate, "
                _sqlInsertAppt += "ReservationStartHour, ReservationStartMinute, AppointmentDuration, DoseNumber)"
                _sqlInsertAppt += "VALUES ('" + str(Vaccine) + "', " + str(self.PatientId) + ", " + str(_CaregiverId) + ", '"
                _sqlInsertAppt += str(_ReservationDate) + "', " + str(_ReservationStartHour) + ", " + str(_ReservationStartMinute)
                _sqlInsertAppt += ", " + str(_AppointmentDuration) + ", " + str(_DoseNumber) + ")"
                # print('Vax appt insert query: ', _sqlInsertAppt)

                cursor.execute(_sqlInsertAppt)

                # store 1st appointment id (for vrs!!!)
                _sqlGetApptInfo = "SELECT * FROM VaccineAppointments WHERE PatientId = " + str(self.PatientId) 
                _sqlGetApptInfo += " AND CaregiverId = " + str(_CaregiverId) + "AND DoseNumber = " + str(_DoseNumber)
                # print('appt info query', _sqlGetApptInfo)

                cursor.execute(_sqlGetApptInfo)
                apptID_row = cursor.fetchone()

                _1stApptId = apptID_row.get('VaccineAppointmentId')

                # update patient status
                _sqlUpdatePatientStatus = "UPDATE Patients SET VaccineStatus = " + str(_UpdatedVaccineStatus) + " WHERE PatientId = " + str(self.PatientId)
                # print('update patient status query: ', _sqlUpdatePatientStatus)

                cursor.execute(_sqlUpdatePatientStatus)
                print('All queries in ReserveAppointments executed!!!!!!')

                # add provision for dose 2

                return _1stApptId # retain class instance from VaccineAppointment slots reserved


        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Vaccine Patient class!")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1]) 
                print("SQL text that resulted in an Error: " + _sqlInsert)
                
    def ScheduleAppointment():
        '''
        Mark Appointments as Scheduled, update the PatientVaccine Status Field, Maintain the Vaccine Inventory
        Update the Caregiver Scheduler Table
        '''
        self.Vaccine = Vaccine
        self.CaregiverSchedulingID = CaregiverSchedulingID

        try:
            # 1st: Update the appointment status from on hold to scheduled
            _sqlCheckApptStatus = "SELECT * FROM CareGiverSchedule WHERE CaregiverSlotSchedulingId = " + str(CaregiverSchedulingID)
            # print('ReserveAppointments check query: ', _sqlCheckApptStatus)

            cursor.execute(_sqlCheckApptStatus)
            appt_row = cursor.fetchone() # should only have 1 row per CaregiverSlotSchedulingId
            # print('appt_row', appt_row)
            
            _CaregiverId = appt_row.get('CaregiverId')
            _ReservationDate = appt_row.get('WorkDay')
            _ReservationStartHour = appt_row.get('SlotHour')
            _ReservationStartMinute = appt_row.get('SlotMinute')
            _SlotStatus = appt_row.get('SlotStatus')
            _AppointmentDuration = 15

            if _SlotStatus == 1: # if SlotStatus = "On Hold", update to scheduled
                _sqlUpdate = "UPDATE CareGiverSchedule SET SlotStatus = " + str(2) + "WHERE SlotStatus = " + str(1) + "AND CaregiverSlotSchedulingId = " + str(CaregiverSchedulingID)
                
                _sqlGetApptInfo = "SELECT * FROM VaccineAppointments WHERE PatientId = " + str(self.PatientId) 
                _sqlGetApptInfo += " AND CaregiverId = " + str(_CaregiverId) + "AND DoseNumber = " + str(_DoseNumber)
                # print('appt info query', _sqlGetApptInfo)

                cursor.execute(_sqlGetApptInfo)
                apptID_row = cursor.fetchone()

                _1stApptId = apptID_row.get('VaccineAppointmentId')

                # update patient status
                _sqlUpdateVaccineSchedule = "UPDATE VaccineAppointments SET SlotStatus = " + str(2) + " WHERE VaccineAppointmentId = " + str(_1stApptId) + "AND SlotStatus = " + str(1)
                # print('update patient status query: ', _sqlUpdatePatientStatus)

                cursor.execute(_sqlUpdateVaccineSchedule)

            # 2nd: get patient details, update patient vaccine status field
            _sqlCheckPatientStatus = "SELECT * FROM Patients WHERE PatientName = '" + str(self.PatientName) + "'" # check if right call
            # print('Patient check query: ', _sqlCheckPatientStatus)

            cursor.execute(_sqlCheckPatientStatus)
            patient_row = cursor.fetchone()
            # print('patient_row', patient_row)

            _VaccineStatus = patient_row.get('VaccineStatus')

            # check if queued for first dose
            if _VaccineStatus == 1: # NEED TO CHECK IF TWO DOSES REQUIRED !!!!!
                # store 1st appointment id (for vrs!!!)
                _sqlGetApptInfo = "SELECT * FROM VaccineAppointments WHERE PatientId = " + str(self.PatientId) 
                _sqlGetApptInfo += " AND CaregiverId = " + str(_CaregiverId) + "AND DoseNumber = " + str(_DoseNumber)
                # print('appt info query', _sqlGetApptInfo)

                cursor.execute(_sqlGetApptInfo)
                apptID_row = cursor.fetchone()

                _1stApptId = apptID_row.get('VaccineAppointmentId')

                # update patient status
                _sqlUpdatePatientStatus = "UPDATE Patients SET VaccineStatus = " + str(_UpdatedVaccineStatus) + " WHERE PatientId = " + str(self.PatientId)
                # print('update patient status query: ', _sqlUpdatePatientStatus)

                cursor.execute(_sqlUpdatePatientStatus)
                print('All queries in ScheduleAppointments executed!!!!!!')

                # add provision for dose 2
            
            covid.ReserveDoses()

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Vaccine Patient class!")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1]) 
                print("SQL text that resulted in an Error: " + _sqlInsert)
