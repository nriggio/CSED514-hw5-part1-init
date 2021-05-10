-- view tables
SELECT * FROM Caregivers;
SELECT * FROM AppointmentStatusCodes;
SELECT * FROM CareGiverSchedule;
SELECT * FROM Vaccines;
SELECT * FROM Patients;
SELECT * FROM VaccineAppointments;

Drop Table CareGiverSchedule;
Drop Table Caregivers;
Drop Table AppointmentStatusCodes;
Drop Table Patients;
Drop Table Vaccines;
Drop Table VaccineAppointments;

EXEC sp_fkeys 'CareGiverSchedule'