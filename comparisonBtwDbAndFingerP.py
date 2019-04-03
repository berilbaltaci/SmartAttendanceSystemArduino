import datetime
import mysql.connector
import serial

try:
    connection = mysql.connector.connect(host='localhost', database='SmartAtt', user='root', password='12345678')
    cursor = connection.cursor()
    ser = serial.Serial('/dev/cu.wchusbserial14310', 9600)
    sql_select_Student_Query = "select * from Student"
    cursor = connection.cursor(buffered=True)
    cursor.execute(sql_select_Student_Query)
    records = cursor.fetchall()

    while True:
        finger = ser.readline()
        if finger != "Waiting for valid finger...\r\n":
            print(finger)
        elif finger == "Waiting for valid finger...\r\n":
            while True:
                print(finger)
                fpId = ser.readline()
                splitString = fpId.split("#", 1)
                fpIdInt = splitString[1].split(" ", 1)
                print(fpIdInt[0])
                for row in records:
                    if str(row[2]) == fpIdInt[0]:
                        sql_select_CourseStudent_query = """SELECT * FROM CourseStudent WHERE StudentId = %s """
                        StudentId = (row[0],)
                        cursor.execute(sql_select_CourseStudent_query, StudentId)
                        recordCS = cursor.fetchone()
                        print(recordCS[0])
                        getDate = datetime.datetime.now()
                        sql_insert_query_AL = """INSERT INTO AttendanceLog
                            (CourseStudentId, Date, IsSchoolCard, IsFingerprint, IsOnline, TeacherId) 
                            VALUES (%s, %s, 1, 1, 0, 1)"""
                        rec = recordCS[0]
                        Input = (rec, getDate)
                        cursor.execute(sql_insert_query_AL, Input)
                        connection.commit()
                        print(row[1])
                        break
                    else:
                        print("Cik disari !!!!")

except mysql.connector.Error as error:
    print("Failed to update record to database: {}".format(error))

finally:
    # closing database connection.
    if connection.is_connected():
        # cursor.close()
        connection.close()
        print("connection is closed")