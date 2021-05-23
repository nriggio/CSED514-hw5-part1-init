from datetime import datetime
from datetime import timedelta
import pymssql

from vaccine_caregiver import VaccineCaregiver
from COVID19_vaccine import COVID19Vaccine as covid
# from vaccine_patient import VaccinePatient as patientS
# from vaccine_reservation_scheduler import VaccineReservationScheduler


class VaccinePatient:
    ''' Initializes adding a patient to be vaccinated. '''
    def __init__(self, PatientName, VaccineStatus, VaccineName, cursor):

        self.PatientName = PatientName
        self.VaccineStatus = VaccineStatus
        self.VaccineName = VaccineName
            
        try:
            _sqlInsert = "INSERT INTO Patients (PatientName, VaccineReceived, VaccineStatus) VALUES ("
            _sqlInsert += "'" + str(PatientName) + "', '" + str(VaccineName) + "', " + str(VaccineStatus) + ")" # PatientName + VaccineStatus

            cursor.execute(_sqlInsert)
            cursor.connection.commit()

            cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            _identityRow = cursor.fetchone()
            self.PatientId = _identityRow['Identity']
            cursor.connection.commit() # needed ???
            print('Query executed successfully. Patient : ' + self.PatientName 
            +  ' added to the database using Patient ID = ' + str(self.PatientId))
            
        except pymssql.Error as db_err:
            cursor.connection.rollback()
            print("Database Programming Error in SQL Query processing for Vaccine Patient class!")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1]) 
                print("SQL text that resulted in an Error: " + _sqlInsert)

    def ReserveAppointment(self, CaregiverSchedulingID, cursor):
        ''' Method to verify if CaregiverSchedulingID = OnHold,
        create initial entry in VaccineAppointment table,
        flag Patient as "queued for dose 1", & create 2nd appointment. 
        * BE SURE TO RETAIN CLASS INSTANCE VARIABLES (i.e. Identity vals from 2 VaccineAppointment slots). '''

        self.CaregiverSchedulingID = CaregiverSchedulingID

        try:
            # 1st: verify that CaregiverSlotSchedulingId passed is "On Hold"
            _sqlCheckApptStatus = "SELECT * FROM CareGiverSchedule WHERE CaregiverSlotSchedulingId = " + str(CaregiverSchedulingID)

            cursor.execute(_sqlCheckApptStatus)
            appt_row = cursor.fetchone() # should only have 1 row per CaregiverSlotSchedulingId
            
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
            _sqlCheckPatientStatus = "SELECT * FROM Patients WHERE PatientName = '" + str(self.PatientName) + "'"

            cursor.execute(_sqlCheckPatientStatus)
            patient_row = cursor.fetchone()

            _VaccineStatus = patient_row.get('VaccineStatus')

            # check if eligible for 1st dose scheduling
            if _VaccineStatus <= 2 and self.VaccineName != 'Johnson & Johnson': # patient still needs 1st dose & only one dose total
                # queue for 1st dose & update patient / vaccine appointment status
                _UpdatedVaccineStatus = 1 # "queued for 1st dose"
                _DoseNumber = 1

            elif _VaccineStatus <=2 and self.VaccineName == 'Johnson & Johnson':
                _UpdatedVaccineStatus = 4 # just mark as queued for 2nd
                _DoseNumber = 1

            elif _VaccineStatus > 2 and _VaccineStatus <= 5: # patient needs 2nd dose
                _UpdatedVaccineStatus = 4 # "queued for 2nd dose"
                _DoseNumber = 2

            else:
                print('Patient is fully vaccinated!')
                raise Exception

            # check already has appointment (no provision for rescheduling)
            _sqlCheckAppt = "SELECT * FROM VaccineAppointments WHERE PatientId = " + str(self.PatientId) + "AND DoseNumber = " + str(_DoseNumber)

            cursor.execute(_sqlCheckAppt)
            checkAppt_row = cursor.fetchone()

            if checkAppt_row == None:
                # create appointment
                _sqlInsertAppt = "INSERT INTO VaccineAppointments (VaccineName, PatientId, CaregiverId, ReservationDate, "
                _sqlInsertAppt += "ReservationStartHour, ReservationStartMinute, AppointmentDuration, SlotStatus, DoseNumber)"
                _sqlInsertAppt += "VALUES ('" + str(self.VaccineName) + "', " + str(self.PatientId) + ", " + str(_CaregiverId) + ", '"
                _sqlInsertAppt += str(_ReservationDate) + "', " + str(_ReservationStartHour) + ", " + str(_ReservationStartMinute)
                _sqlInsertAppt += ", " + str(_AppointmentDuration) + ", " + str(_SlotStatus) + ", " + str(_DoseNumber) + ")"

                cursor.execute(_sqlInsertAppt)

            else:
                print('Patient already has an appointment and this system can\'t handle rescheduling yet (lol)')
                raise Exception

            # store appointment id (for vrs!!!)
            _sqlGetApptInfo = "SELECT * FROM VaccineAppointments WHERE PatientId = " + str(self.PatientId) 
            _sqlGetApptInfo += " AND CaregiverId = " + str(_CaregiverId) + "AND DoseNumber = " + str(_DoseNumber)

            cursor.execute(_sqlGetApptInfo)
            apptID_row = cursor.fetchone()

            _ApptId = apptID_row.get('VaccineAppointmentId')

            # update patient status
            _sqlUpdatePatientStatus = "UPDATE Patients SET VaccineStatus = " + str(_UpdatedVaccineStatus) + " WHERE PatientId = " + str(self.PatientId)

            cursor.execute(_sqlUpdatePatientStatus)
            cursor.connection.commit()
            # print('All queries in ReserveAppointments passed!!!!!!')

            # print('appt id to schedule:', _ApptId)

            # return _ApptId, _2ndApptId # retain class instance from VaccineAppointment slots reserved
            return _ApptId

        except pymssql.Error as db_err:
            cursor.connection.rollback()
            print("Database Programming Error in SQL Query processing for Vaccine Patient class!")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1]) 
                print("SQL text that resulted in an Error: " + _sqlUpdatePatientStatus)
                
    def ScheduleAppointment(self, CaregiverSchedulingID, cursor):  #Vaccine, cursor):
        '''
        Mark Appointments as Scheduled, update the PatientVaccine Status Field, Maintain the Vaccine Inventory
        Update the Caregiver Scheduler Table
        '''
        self.CaregiverSchedulingID = CaregiverSchedulingID

        try:
            # check if enough doses to schedule
            _AvailableDoses = covid.ReserveDoses(self = self, cursor = cursor)
            print('output reservedoses: ', _AvailableDoses)

            # 1st: Update the appointment status from on hold to scheduled
            _sqlCheckApptStatus = "SELECT * FROM CareGiverSchedule WHERE CaregiverSlotSchedulingId = " + str(CaregiverSchedulingID)

            cursor.execute(_sqlCheckApptStatus)
            appt_row = cursor.fetchone() 
            
            _CaregiverId = appt_row.get('CaregiverId')
            _SlotStatus = appt_row.get('SlotStatus')

            if _SlotStatus == 1: # if SlotStatus = "On Hold", update to scheduled
                _sqlUpdate = "UPDATE CareGiverSchedule SET SlotStatus = " + str(2) + "WHERE SlotStatus = " + str(1) + "AND CaregiverSlotSchedulingId = " + str(CaregiverSchedulingID)
                cursor.execute(_sqlUpdate)
                cursor.connection.commit()

            _sqlGetApptInfo = "SELECT * FROM VaccineAppointments WHERE PatientId = " + str(self.PatientId) 
            _sqlGetApptInfo += " AND CaregiverId = " + str(_CaregiverId) #+ "AND DoseNumber = " + str(_DoseNumber)

            cursor.execute(_sqlGetApptInfo)
            apptID_row = cursor.fetchone()

            _ApptId = apptID_row.get('VaccineAppointmentId')

            if _ApptId >= 0 and _AvailableDoses >=2:

                # update patient status
                _sqlUpdateVaccineSchedule = "UPDATE VaccineAppointments SET SlotStatus = " + str(2) + " WHERE VaccineAppointmentId = " + str(_ApptId) #+ "AND SlotStatus = " + str(1)

                cursor.execute(_sqlUpdateVaccineSchedule)
                cursor.connection.commit()

            # 2nd: get patient details, update patient vaccine status field
            _sqlCheckPatientStatus = "SELECT * FROM Patients WHERE PatientName = '" + str(self.PatientName) + "'" # check if right call

            cursor.execute(_sqlCheckPatientStatus)
            patient_row = cursor.fetchone()

            _VaccineStatus = patient_row.get('VaccineStatus')

            # check if queued for first dose
            if _VaccineStatus == 1: # NEED TO CHECK IF TWO DOSES REQUIRED !!!!!
                # store 1st appointment id (for vrs!!!)
                _sqlGetApptInfo = "SELECT * FROM VaccineAppointments WHERE PatientId = " + str(self.PatientId) 
                _sqlGetApptInfo += " AND CaregiverId = " + str(_CaregiverId) #+ "AND DoseNumber = " + str(_DoseNumber)

                cursor.execute(_sqlGetApptInfo)
                apptID_row = cursor.fetchone()

                _ApptId = apptID_row.get('VaccineAppointmentId')

                _UpdatedVaccineStatus = 2 # "1st dose scheduled"

                # update patient status
                _sqlUpdatePatientStatus = "UPDATE Patients SET VaccineStatus = " + str(_UpdatedVaccineStatus) + " WHERE PatientId = " + str(self.PatientId)

                cursor.execute(_sqlUpdatePatientStatus)
                cursor.connection.commit()
                # print('All queries in ScheduleAppointments passed!!!!!!')

                # add provision for dose 2

        except pymssql.Error as db_err:
            cursor.connection.rollback()
            print("Database Programming Error in SQL Query processing for Vaccine Patient class!")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1]) 
                print("SQL text that resulted in an Error: " + _sqlUpdatePatientStatus)
