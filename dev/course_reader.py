import csv
import psycopg2

PG_USER = "postgres"
PG_USER_PASS = "41740284"
PG_DATABASE = "course1"
PG_HOST_INFO = " host=/tmp/" # use "" for OS X or Windows

def load_course_database(db_name, csv_filename):
    with open(csv_filename+'.csv', 'rU') as csvfile:
        conn = psycopg2.connect("dbname="+PG_DATABASE + " user=" + PG_USER + " password=" + PG_USER_PASS + PG_HOST_INFO)
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS coursedata;")
        cur.execute("CREATE TABLE coursedata (deptID text, courseNum int, semester int, meetingType text, seatsTaken int, seatsOffered int, instructor text);")
        reader = csv.reader(csvfile)
        for row in reader:
            cur.execute("INSERT INTO coursedata (deptID, courseNum, semester, meetingType, seatsTaken, seatsOffered, instructor) VALUES (%s, %s, %s, %s, %s, %s, %s);", tuple(row))
        conn.commit()
        cur.close()
        conn.close()

if __name__ == "__main__":
    load_course_database(PG_USER,"seas-courses-5years")