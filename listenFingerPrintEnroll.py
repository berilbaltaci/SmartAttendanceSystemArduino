import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import serial
import sys

try:
    connection = mysql.connector.connect(host='localhost', database='SmartAtt', user='root', password='12345678')
    cursor = connection.cursor()
    ser = serial.Serial('/dev/cu.wchusbserial14110', 9600)
    sql_update_query = """ UPDATE `Fingerprint` SET FingerprintData=%s WHERE FingerprintId=%s"""

    while True:
        FingerprintData = ser.readline()  # type: str
        if FingerprintData == "Please type in the ID # (from 1 to 127) you want to save this finger as...\r\n":
            fpId = raw_input("enter an id: ")
            fpIdInt = int(fpId)
            ser.write(fpId)
            input = (fpId, FingerprintId)
            cursor.execute(sql_update_query, input)
            connection.commit()
        FingerprintId = 3
        if FingerprintData:
            print(FingerprintData)
           # input = (FingerprintData, FingerprintId)
            #cursor.execute(sql_update_query, input)
           # connection.commit()


except mysql.connector.Error as error:

    # connection.rollback() #rollback if any exception occured
    print("Failed to update record to database: {}".format(error))

finally:
    # closing database connection.
    if connection.is_connected():
        # cursor.close()
        connection.close()
        print("connection is closed")
