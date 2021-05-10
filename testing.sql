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

-- TEST Vaccine addition queries
INSERT INTO Vaccines (VaccineName, DosesRequired, MaxSpacing, MinSpacing, MaxStorageTemp) 
VALUES ('Johnson & Johnson', '1', '0', '0', '0');

UPDATE Vaccines SET TotalDoses = TotalDoses + 100 WHERE VaccineName = 'Johnson & Johnson';

SELECT * FROM Vaccines WHERE VaccineName = 'Johnson & Johnson'