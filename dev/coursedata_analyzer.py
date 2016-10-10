import psycopg2
import sys

PG_USER = "postgres"
<<<<<<< HEAD
PG_USER_PASS = "555555"#asdf
=======
PG_USER_PASS = sys.argv[1]
>>>>>>> origin/master
PG_DATABASE = "course1"
PG_HOST_INFO = " host=/tmp/" # use "" for OS X or Windows

departmentDict = {}

def instructor_numbers(dept_id):
    conn = psycopg2.connect("dbname=" + PG_DATABASE + " user=" + PG_USER + " password=" + PG_USER_PASS + PG_HOST_INFO)
    cur = conn.cursor()
    cur.execute("SELECT * FROM coursedata WHERE deptID=%s;", (dept_id,))
    row = cur.fetchone()
    while row != None:
        if row[6] not in departmentDict:
            departmentDict.update({row[6]:row[4]})
        else:
            departmentDict[row[6]] = departmentDict[row[6]] + row[4]
        row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    for key in departmentDict:
        print(key, ": ", departmentDict[key])

if __name__ == "__main__":
    instructor_numbers("APMA")
