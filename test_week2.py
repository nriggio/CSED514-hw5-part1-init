import unittest
import os

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from COVID19_vaccine import COVID19Vaccine as covid
from vaccine_patient import VaccinePatient as patient
from vaccine_reservation_scheduler import VaccineReservationScheduler

class TestDB(unittest.TestCase):

    def test_db_connection(self):
        try:
            self.connection_manager = SqlConnectionManager(Server=os.getenv("Server"),
                                                           DBname=os.getenv("DBName"),
                                                           UserId=os.getenv("UserID"),
                                                           Password=os.getenv("Password"))
            self.conn = self.connection_manager.Connect()
        except Exception:
            self.fail("Connection to database failed")


class TestVaccineReservationScheduler(unittest.TestCase):
    def test_PutAppointmentOnHold(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                DBname=os.getenv("DBName"),
                                UserId=os.getenv("UserID"),
                                Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # create vaccine object
                    self.covid = covid(VaccineName = "Pfizer", cursor = cursor)

                    # create caretaker object
                    self.caregiver = VaccineCaregiver(name = "Clare Barton", cursor = cursor)

                    # create patient object
                    self.patient = patient(PatientName = 'Nicole Riggio', VaccineStatus = 0, VaccineName = 'Pfizer', cursor = cursor)

                    # Put appointment on hold
                    vrs = VaccineReservationScheduler()
                    self.vrs = vrs.PutHoldOnAppointmentSlot(cursor = cursor)

                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT *
                               FROM CareGiverSchedule
                               WHERE SlotStatus = 1
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if len(rows) == 1 and rows[0].get('SlotStatus') == 1: 
                        print('PutAppointmentOnHold worked!')

                    else:
                        self.fail('PutAppointmentOnHold failed')

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)

                    self.fail("PutAppointmentOnHold failed due to exception")

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("The appointment was NOT put on hold.")

    def test_ScheduleAppointmentSlot(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                DBname=os.getenv("DBName"),
                                UserId=os.getenv("UserID"),
                                Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # create vaccine object
                    self.covid = covid(VaccineName = "Pfizer", cursor = cursor)

                    # create caretaker object
                    self.caregiver = VaccineCaregiver(name = "Clare Barton", cursor = cursor)

                    # create patient object
                    self.patient = patient(PatientName = 'Nicole Riggio', VaccineStatus = 0, VaccineName = 'Pfizer', cursor = cursor)

                    # put appointment on hold
                    vrs = VaccineReservationScheduler()
                    self.vrs = vrs.PutHoldOnAppointmentSlot(cursor = cursor)

                    # schedule appointment
                    self.vrs = vrs.ScheduleAppointmentSlot(slotid = 1, cursor = cursor)

                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT *
                               FROM CareGiverSchedule
                               WHERE SlotStatus = 2
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if len(rows) == 1 and rows[0].get('SlotStatus') == 2: 
                        print('ScheduleAppointmentSlot worked!')

                    else:
                        self.fail('ScheduleAppointmentSlot failed')

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)

                    self.fail("ScheduleAppointmentSlot failed due to exception")

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("The appointment was NOT properly scheduled.")


class TestVaccinePatient(unittest.TestCase):
    def test_patient_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # create a new Vaccine object
                    self.covid = covid(VaccineName = "Pfizer", cursor = cursor)

                    # create a new Patient object
                    self.patient = patient(PatientName = 'Nicole Riggio', VaccineStatus = 0, VaccineName = 'Pfizer', cursor = cursor)

                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT *
                               FROM Patients
                               WHERE PatientName = 'Nicole Riggio'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if len(rows) != 1: 
                        self.fail("Creating patient failed")

                    elif len(rows) == 1:
                        print('Patient was added initialized in Patients!')

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)

                    self.fail("Creating patient failed due to exception")

    def test_ReserveAppointment(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # create vaccine object
                    self.covid = covid(VaccineName = "Pfizer", cursor = cursor)

                    # create caretaker object
                    self.caregiver = VaccineCaregiver(name = "Clare Barton", cursor = cursor)

                    # create patient object
                    self.patient = patient(PatientName = 'Nicole Riggio', VaccineStatus = 0, VaccineName = 'Pfizer', cursor = cursor)

                    # put appointment on hold
                    vrs = VaccineReservationScheduler()
                    # self.vrs = vrs.PutHoldOnAppointmentSlot(cursor = cursor)

                    # reserve the appointment
                    self.patient.ReserveAppointment(CaregiverSchedulingID = vrs.PutHoldOnAppointmentSlot(cursor = cursor), cursor = cursor)

                    # check if the appointment is marked as reserved & patient status is updated
                    sqlQuery = '''
                               SELECT *
                               FROM VaccineAppointments
                               WHERE PatientId = 1
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if len(rows) == 1 and rows[0].get('SlotStatus') == 1: 
                        # print('Appt marked as reserved!')

                        sqlQuery = '''
                                SELECT *
                                FROM Patients
                                WHERE PatientName = 'Nicole Riggio'
                                '''
                        cursor.execute(sqlQuery)
                        rows = cursor.fetchall()

                        if len(rows) == 1 and rows[0].get('VaccineStatus') == 1:
                            print('Patient queued for vaccine dose!')

                        else:
                            self.fail('Patient status not updated.')

                    else:
                        self.fail('Slot status not updated.')

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)

                    self.fail("ReserveAppointment failed due to exception")
    
    def test_ScheduleAppointment(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    
                    # create vaccine object
                    self.covid = covid(VaccineName = "Pfizer", cursor = cursor)
                    
                    # Add doses to vaccine object
                    self.covid.AddDoses(DosesToAdd = 5, cursor = cursor)

                    # create caretaker object
                    self.caregiver = VaccineCaregiver(name = "Clare Barton", cursor = cursor)

                    # create patient object
                    self.patient = patient(PatientName = 'Alyson Suchodolski', VaccineStatus = 0, VaccineName = 'Pfizer', cursor = cursor)
                    
                    # Schedule the appointment
                    vrs = VaccineReservationScheduler()
                    self.patient.ReserveAppointment(CaregiverSchedulingID = vrs.PutHoldOnAppointmentSlot(cursor = cursor), cursor = cursor)
                    self.patient.ScheduleAppointment(CaregiverSchedulingID = vrs.ScheduleAppointmentSlot(slotid = 1, cursor=cursor), cursor = cursor)
                    
                    # Check if the appointment was scheduled & the patient status was updated
                    sqlQuery = '''
                               SELECT *
                               FROM VaccineAppointments
                               WHERE PatientId = 1
                               '''

                    # sqlQuery = '''
                    #            SELECT *
                    #            FROM CaregiverSchedule
                    #            WHERE SlotStatus = 2
                    #            '''

                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    
                    if len(rows) == 1 and rows[0].get('SlotStatus') == 2:
                        print('Appointment Marked as Scheduled!')
                        
                        sqlQuery = '''
                                   SELECT *
                                   FROM Patients
                                   WHERE PatientName = 'Alyson Suchodolski'
                                   '''
                        cursor.execute(sqlQuery)
                        rows = cursor.fetchall()
                        
                        if len(rows) == 1 and rows[0].get('VaccineStatus') == 2:
                            print('First Dose Scheduled!')
                            
                            sqlQuery = '''
                                       Select *
                                       FROM Vaccines
                                       WHERE VaccineName = 'Pfizer'
                                       '''
                            cursor.execute(sqlQuery)
                            rows = cursor.fetchall()
                            
                            if len(rows) == 1 and rows[0].get('ReservedDoses') == 2 and rows[0].get('AvailableDoses') == 3:
                                print('Vaccine inventory has been updated!')
                            
                            else:
                                self.fail('Vaccine inventory could not be updated!')
                            
                        else:
                            self.fail('Patient status not updated!')
                    
                    else:
                        self.fail('Slot status not updated!')
                
                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)

                    self.fail("ScheduleAppointment failed due to exception")

    def test_allocate2caregivers(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # create caretaker object
                    caregiversList = []
                    caregiversList.append(VaccineCaregiver('Carrie Nation', cursor)) # allocates at least 2 caregivers
                    caregiversList.append(VaccineCaregiver('Clare Barton', cursor))
                    caregivers = {}
                    for cg in caregiversList:
                        cgid = cg.caregiverId
                        caregivers[cgid] = cg

                    # check two caregivers have been created
                    sqlQuery = '''
                               SELECT *
                               FROM Caregivers
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if len(rows) == 2: 
                        print('Two caregivers were created!')

                    else:
                        self.fail('Failed to create two caregivers.')

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)

                    self.fail("Creating caregivers failed due to exception.")

    def test_add5doses(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # create vaccine object
                    self.covid = covid(VaccineName = "Pfizer", cursor = cursor)
                    self.covid.AddDoses(DosesToAdd = 5, cursor = cursor)

                    # check if the doses were added
                    sqlQuery = '''
                               SELECT *
                               FROM Vaccines
                               WHERE VaccineName = 'Pfizer' AND AvailableDoses = 5 AND TotalDoses = 5
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()

                    if len(rows) == 1: 
                        print('Doses were added successfully!')

                    else:
                        self.fail('Vaccine doses were not added.')

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)

                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)

                    self.fail("Vaccine doses failed due to exception.")

    def test_schedule2Patients(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    
                    # create vaccine object
                    self.covid = covid(VaccineName = "Pfizer", cursor = cursor)
                    
                    # Add doses to vaccine object
                    self.covid.AddDoses(DosesToAdd = 5, cursor = cursor)

                    # create caretaker object
                    self.caregiver = VaccineCaregiver(name = "Clare Barton", cursor = cursor)
                    self.caregiver = VaccineCaregiver(name = "Carrie Nation", cursor = cursor)
                    
                    # create patient object
                    self.patient1 = patient(PatientName = 'Alyson Suchodolski', VaccineStatus = 1, VaccineName = 'Pfizer', cursor = cursor)
                    self.patient2 = patient(PatientName = 'Nicole Riggio', VaccineStatus = 1, VaccineName = 'Pfizer', cursor = cursor)
                    self.patient3 = patient(PatientName = 'Jameson Reagan', VaccineStatus = 1, VaccineName = 'Pfizer', cursor = cursor)
                    self.patient4 = patient(PatientName = 'Arianna Pilla', VaccineStatus = 1, VaccineName = 'Pfizer', cursor = cursor)
                    self.patient5 = patient(PatientName = 'Christopher Martone', VaccineStatus = 1, VaccineName = 'Pfizer', cursor = cursor)
                    
                    # reserve slots for patients, then schedule slots
                    vrs = VaccineReservationScheduler()
                    p1d1 = self.patient1.ReserveAppointment(CaregiverSchedulingID = vrs.PutHoldOnAppointmentSlot(cursor = cursor), cursor = cursor)
                    self.patient1.ScheduleAppointment(CaregiverSchedulingID = vrs.ScheduleAppointmentSlot(slotid = p1d1, cursor = cursor), cursor = cursor)
                    
                    p2d1 = self.patient2.ReserveAppointment(CaregiverSchedulingID = vrs.PutHoldOnAppointmentSlot(cursor = cursor), cursor = cursor)
                    self.patient2.ScheduleAppointment(CaregiverSchedulingID = vrs.ScheduleAppointmentSlot(slotid = p2d1, cursor = cursor), cursor = cursor)
                    
                    p3d1 = self.patient3.ReserveAppointment(CaregiverSchedulingID = vrs.PutHoldOnAppointmentSlot(cursor = cursor), cursor = cursor)
                    self.patient3.ScheduleAppointment(CaregiverSchedulingID = vrs.ScheduleAppointmentSlot(slotid = p3d1, cursor = cursor), cursor = cursor)
                    
                    p4d1 = self.patient4.ReserveAppointment(CaregiverSchedulingID = vrs.PutHoldOnAppointmentSlot(cursor = cursor), cursor = cursor)
                    self.patient4.ScheduleAppointment(CaregiverSchedulingID = vrs.ScheduleAppointmentSlot(slotid = p4d1, cursor = cursor), cursor = cursor)
                    
                    p5d1 = self.patient5.ReserveAppointment(CaregiverSchedulingID = vrs.PutHoldOnAppointmentSlot(cursor = cursor), cursor = cursor)
                    self.patient5.ScheduleAppointment(CaregiverSchedulingID = vrs.ScheduleAppointmentSlot(slotid = p5d1, cursor = cursor), cursor = cursor)
                    
                    # check if only two rows were updated
                    sqlQuery = '''
                               SELECT *
                               FROM VaccineAppointments
                               WHERE SlotStatus = 2
                               '''
                    
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    
                    if len(rows) == 2:
                        print('Only 2 patients could be scheduled for appointments!')
                    
                    else:
                        self.fail('Scheduling System Failed!: Too many or not enough appointments were made.')
                    
                    clear_tables(sqlClient)
                
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)

                    self.fail("Scheduling Appointments failed due to exception.")



if __name__ == '__main__':
    unittest.main()
