# coding: utf8
import sys
import json
import sqlite3


CONN = sqlite3.connect("dlls.db")
CURSOR = CONN.cursor()


def initDB():
    sql = "CREATE TABLE IF NOT EXISTS dlls(id INTEGER PRIMARY KEY,DLLName VARCHAR(255)," \
          "CompanyName VARCHAR(255),FileVersion VARCHAR(255)," \
          "LegalCopyright VARCHAR(255),FileDescription TEXT)"
    CURSOR.execute(sql)
    CONN.commit()


def insertDLLs(properties):
    sql = "INSERT INTO dlls values(?,?,?,?,?,?)"
    CURSOR.executemany(sql, properties)
    CONN.commit()


def loadJson(fileName):
    initDB()
    with open(fileName, "r") as fp:
        count = 0
        properties = []
        content = fp.read()
        obj = json.loads(content)
        for dllName in obj:
            prop = (None, dllName, obj[dllName]["CompanyName"], obj[dllName]["FileVersion"],
                    obj[dllName]["LegalCopyright"], obj[dllName]["FileDescription"])
            properties.append(prop)
            count += 1
        insertDLLs(properties)
    pass


if __name__ == '__main__':
    fileName = sys.argv[1]
    loadJson(fileName)
    CURSOR.close()
    CONN.close()
