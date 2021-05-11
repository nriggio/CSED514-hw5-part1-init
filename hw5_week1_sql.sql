CREATE PROCEDURE InitDataModel
AS

-- Caregivers Table
Create Table Caregivers(
    CaregiverId int IDENTITY PRIMARY KEY,
    CaregiverName varchar(50)
    );

-- AppointmentStatusCodes Table
Create Table AppointmentStatusCodes(
    StatusCodeId int PRIMARY KEY,
    StatusCode   varchar(30)
);

-- Populate AppointmentStatusCodes
INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
    VALUES (0, 'Open');
INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
    VALUES (1, 'OnHold');
INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
    VALUES (2, 'Scheduled');
INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
    VALUES (3, 'Completed');
INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
    VALUES (4, 'Missed');

-- Vaccines Table
CREATE TABLE Vaccines(
    VaccineId int IDENTITY PRIMARY KEY,
    VaccineName varchar(50),
    DosesRequired int,
    MaxSpacing int,
    MinSpacing int,
    MaxStorageTemp varchar(50),
    DosesAvailable int DEFAULT 0 NOT NULL,
    DosesReserved int DEFAULT 0 NOT NULL
);


-- Patients Table
CREATE TABLE Patients(
    PatientId int IDENTITY PRIMARY KEY,
    PatientName varchar(50),
    DOB date,
    PhoneNumber varchar(50),
    Email varchar(50),
    VaccineReceived int FOREIGN KEY REFERENCES Vaccines(VaccineId),
    DosesReceived int DEFAULT 0 NOT NULL --- need key ????
);

-- CaregiverSchedule Table
Create Table CareGiverSchedule(
    CaregiverSlotSchedulingId int Identity PRIMARY KEY, 
    CaregiverId int DEFAULT 0 NOT NULL
        CONSTRAINT FK_CareGiverScheduleCaregiverId FOREIGN KEY (caregiverId)
            REFERENCES Caregivers(CaregiverId),
    WorkDay date,
    -- SlotTime time,
    SlotHour int DEFAULT 0 NOT NULL,
    SlotMinute int DEFAULT 0 NOT NULL,
    SlotStatus int  DEFAULT 0 NOT NULL
        CONSTRAINT FK_CaregiverStatusCode FOREIGN KEY (SlotStatus) 
            REFERENCES AppointmentStatusCodes(StatusCodeId)
    --VaccineAppointmentId int DEFAULT 0 NOT NULL
    -- PatientId int FOREIGN KEY REFERENCES Patients(PatientId)
    );

-- VaccineAppointments Table
CREATE TABLE VaccineAppointments(
    VaccineAppointmentId int IDENTITY PRIMARY KEY,
    PatientId int FOREIGN KEY REFERENCES Patients(PatientId),
    VaccineId int  FOREIGN KEY REFERENCES Vaccines(VaccineId),
    -- DoseNumber int DEFAULT 1,
    CaregiverSlotSchedulingId int FOREIGN KEY 
        REFERENCES CareGiverSchedule(CaregiverSlotSchedulingId),
    StatusCodeId int FOREIGN KEY REFERENCES AppointmentStatusCodes(StatusCodeId)
);

GO

EXEC InitDataModel;


-- -- Additional helper code for your use if needed

-- --- Select tables
-- SELECT * FROM Caregivers
-- SELECT * FROM AppointmentStatusCodes;
-- SELECT * FROM CareGiverSchedule;
-- SELECT * FROM Vaccines;
-- SELECT * FROM Patients;
-- SELECT * FROM VaccineAppointments;

-- -- --- Drop stored procedure
-- DROP PROCEDURE InitDataModel;
-- GO

-- --- Drop commands to restructure the DB
-- Drop Table CareGiverSchedule;
-- Drop Table Caregivers;
-- Drop Table AppointmentStatusCodes;
-- Drop Table Patients;
-- Drop Table Vaccines;
-- Drop Table VaccineAppointments;

-- --- Commands to clear the active database Tables for unit testing
-- Truncate Table CareGiverSchedule
-- DBCC CHECKIDENT ('CareGiverSchedule', RESEED, 0)
-- Delete From Caregivers
-- DBCC CHECKIDENT ('Caregivers', RESEED, 0)
-- GO

