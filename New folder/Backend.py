"""
Back-End of TDS Database Application

"""

import psycopg2

def connect1():
    conn=psycopg2.connect("dbname='TDS' user='postgres' password='Quest1234' host='172.18.50.178' port='5432'")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS TDS_Data(SOR Text NOT NULL, TDS Text NOT NULL, Issue Text NOT NULL, TDSNo Text PRIMARY KEY, StartDate Date NOT NULL, EndDate Date NOT NULL, Geography Text NOT NULL, Status Text NOT NULL, NonExpHrs Real NOT NULL, OnExpHrs Real NOT NULL, OffExpHrs Real NOT NULL, OffPerHrs Real NOT NULL, TarPerHrs Real NOT NULL, Remarks Text NOT NULL)")
    conn.commit()
    conn.close()

def connect2():
    conn=psycopg2.connect("dbname='TDS' user='postgres' password='Quest1234' host='172.18.50.178' port='5432'")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS TDS_Backup(SOR Text NOT NULL, TDS Text NOT NULL, Issue Text NOT NULL, TDSNo Text NOT NULL, StartDate Date NOT NULL, EndDate Date NOT NULL, Geography Text NOT NULL, Status Text NOT NULL, NonExpHrs Real NOT NULL, OnExpHrs Real NOT NULL, OffExpHrs Real NOT NULL, OffPerHrs Real NOT NULL, TarPerHrs Real NOT NULL, Remarks Text NOT NULL)")
    conn.commit()
    conn.close()

def insert(SOR, TDS, Issue, TDSNo, StartDate, EndDate, Geography, Status, NonExpHrs, OnExpHrs, OffExpHrs, OffPerHrs, TarPerHrs, Remarks):
    conn=psycopg2.connect("dbname='TDS' user='postgres' password='Quest1234' host='172.18.50.178' port='5432'")
    cur=conn.cursor()
    try:
        cur.execute("INSERT INTO TDS_Data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (SOR, TDS, Issue, TDSNo, StartDate, EndDate, Geography, Status, NonExpHrs, OnExpHrs, OffExpHrs, OffPerHrs, TarPerHrs, Remarks))
        conn.commit()
        conn.close()
    except psycopg2.Error as e:
        conn.close()
        return e.pgcode
        pass
    
def view():
    conn=psycopg2.connect("dbname='TDS' user='postgres' password='Quest1234' host='172.18.50.178' port='5432'")
    cur=conn.cursor()
    cur.execute("SELECT * FROM TDS_Data ORDER BY TDSNo")
    rows=cur.fetchall()
    conn.close()
    return rows

def search(SOR, TDS, Issue, TDSNo, StartDate, EndDate, Geography, Status, NonExpHrs, OnExpHrs, OffExpHrs, OffPerHrs, TarPerHrs, Remarks):
    conn=psycopg2.connect("dbname='TDS' user='postgres' password='Quest1234' host='172.18.50.178' port='5432'")
    cur=conn.cursor()
    cur.execute("""SELECT * FROM TDS_Data WHERE SOR=%s or TDS=%s or Issue=%s or 
                StartDate=%s or EndDate=%s or Geography=%s or Status=%s or NonExpHrs=%s or 
                OnExpHrs=%s or OffExpHrs=%s or OffPerHrs=%s or TarPerHrs=%s or Remarks=%s"""
                , (SOR, TDS, Issue, StartDate, EndDate, Geography, Status, NonExpHrs, OnExpHrs, OffExpHrs, OffPerHrs, TarPerHrs, Remarks))
    rows=cur.fetchall()
    conn.close()
    return rows

def delete(TDSNum):
    conn=psycopg2.connect("dbname='TDS' user='postgres' password='Quest1234' host='172.18.50.178' port='5432'")
    cur=conn.cursor()
    cur.execute("DELETE FROM TDS_Data WHERE TDSNo=%s", [TDSNum])
    #cursor.execute("""SELECT name FROM %s.customer WHERE firm_id=%%s""" % schema, each['id'])
    conn.commit()
    conn.close()

def update(TDSNo, StartDate, EndDate, Geography, Status, NonExpHrs, OnExpHrs, OffExpHrs, OffPerHrs, TarPerHrs, Remarks):
    conn=psycopg2.connect("dbname='TDS' user='postgres' password='Quest1234' host='172.18.50.178' port='5432'")
    cur=conn.cursor()
    cur.execute("UPDATE TDS_Data SET StartDate=%s, EndDate=%s, Geography=%s, Status=%s, NonExpHrs=%s, OnExpHrs=%s, OffExpHrs=%s, OffPerHrs=%s, TarPerHrs=%s, Remarks=%s WHERE TDSNo=%s", (StartDate, EndDate, Geography, Status, NonExpHrs, OnExpHrs, OffExpHrs, OffPerHrs, TarPerHrs, Remarks, TDSNo))
    conn.commit()
    conn.close()

def getsordata(sorno):
    conn=psycopg2.connect("dbname='TDS' user='postgres' password='Quest1234' host='172.18.50.178' port='5432'")
    cur=conn.cursor()
    cur.execute("SELECT * FROM sortable WHERE sor=%s", (sorno))
    rows=cur.fetchall()
    conn.close()
    return rows

def backup1(TDSNo):
    conn=psycopg2.connect("dbname='TDS' user='postgres' password='Quest1234' host='172.18.50.178' port='5432'")
    cur=conn.cursor()
    cur.execute("SELECT * FROM TDS_Data WHERE TDSNo LIKE %s", [TDSNo])
    rows=cur.fetchall()
    conn.close()
    return rows

def backup2(SOR, TDS, Issue, TDSNo, StartDate, EndDate, Geography, Status, NonExpHrs, OnExpHrs, OffExpHrs, OffPerHrs, TarPerHrs, Remarks):
    conn=psycopg2.connect("dbname='TDS' user='postgres' password='Quest1234' host='localhost' port='5432'")
    cur=conn.cursor()
    cur.execute("INSERT INTO TDS_Backup VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (SOR, TDS, Issue, TDSNo, StartDate, EndDate, Geography, Status, NonExpHrs, OnExpHrs, OffExpHrs, OffPerHrs, TarPerHrs, Remarks))
    conn.commit()
    conn.close()

def backup3(TDSNo):
    conn=psycopg2.connect("dbname='TDS' user='postgres' password='Quest1234' host='localhost' port='5432'")
    cur=conn.cursor()
    cur.execute("DELETE FROM TDS_Data WHERE TDSNo=%s", [TDSNo])
    conn.commit()
    conn.close()
    
def exportdata(data):
    conn=psycopg2.connect("dbname='TDS' user='postgres' password='Quest1234' host='localhost' port='5432'")
    cur=conn.cursor()
    if data=="Current Data":
        cur.execute("SELECT * FROM TDS_Data ORDER BY TDSNo")
    elif data=="Backup Data":
        cur.execute("SELECT * FROM TDS_Backup ORDER BY TDSNo")
    rows=cur.fetchall()
    conn.close()
    return rows

connect1()
connect2()
