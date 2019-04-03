import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import serial

try:
    connection = mysql.connector.connect(host='localhost', database='SmartAtt', user='root', password='12345678')
    sql_select_Student_Query = "select * from Student"
    cursor = connection.cursor()
    cursor.execute(sql_select_Student_Query)
    records = cursor.fetchall()
    ser = serial.Serial('/dev/cu.wchusbserial14130', 9600)

    while True:
        CardId = ser.readline()  # type: str
        print(CardId)
        for row in records:
            if row[3] == CardId:
                # sql_select_User_Query = "SELECT * FROM User WHERE UserId = %s"
                # UserId = (row[1], )
                # cursor = connection.cursor(buffered=True)
                # cursor.execute(sql_select_User_Query, UserId)
                # record = cursor.fetchone()
                sql_select_CourseStudent_query = """SELECT * FROM CourseStudent WHERE StudentId = %s """
                StudentId = (row[0], )
                cursor.execute(sql_select_CourseStudent_query, StudentId)
                recordCS = cursor.fetchone()
                print(recordCS[0])
                sql_insert_AttendanceLog_query = """INSERT INTO AttendanceLog 
                (CourseStudentId, Date, IsSchoolCard, IsFingerprint, IsOnline, TeacherId) 
                                                VALUES (%s, "14/3/2019", 1, 0, 0, 1)"""
                CourseStudentId = (recordCS[0], )
                cursor.execute(sql_insert_AttendanceLog_query, CourseStudentId)
                connection.commit()

except mysql.connector.Error as error:
    print("Failed to update record to database: {}".format(error))

finally:
    # closing database connection.
    if connection.is_connected():
        # cursor.close()
        connection.close()
        print("connection is closed")