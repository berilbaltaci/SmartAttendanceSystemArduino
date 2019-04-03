import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import serial
try:
   connection = mysql.connector.connect(host='localhost', database='SmartAtt', user='root', password='12345678')
   cursor = connection.cursor()
   ser = serial.Serial('/dev/cu.wchusbserial14130', 9600)
   sql_update_query = """ UPDATE `Student` SET CardId=%s WHERE StudentId=%s"""

   while True:
        CardId = ser.readline()  # type: str
        StudentId = 3
        if CardId:
            print(CardId)
            input = (CardId, StudentId)
            cursor.execute(sql_update_query, input)
            connection.commit()

   print("Record Updated successfully with prepared statement")
except mysql.connector.Error as error :
    #connection.rollback() #rollback if any exception occured
    print("Failed to update record to database: {}".format(error))
finally:
    #closing database connection.
    if connection.is_connected():
        #cursor.close()
        connection.close()
        print("connection is closed")

