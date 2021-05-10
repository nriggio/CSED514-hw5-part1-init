def clear_tables(client):
    sqlQuery = '''
               DELETE FROM CareGiverSchedule
               DBCC CHECKIDENT ('CareGiverSchedule', RESEED, 0)

               DELETE FROM Caregivers
               DBCC CHECKIDENT ('Caregivers', RESEED, 0)

               DELETE FROM Vaccines
               DBCC CHECKIDENT('Vaccines', RESEED, 0)
               '''
    client.cursor().execute(sqlQuery)
    client.commit()

## Truncate Table CareGiverSchedule
## https://stackoverflow.com/questions/253849/cannot-truncate-table-because-it-is-being-referenced-by-a-foreign-key-constraint