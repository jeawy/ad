#!/usr/bin/python
# -*- coding: cp1252 -*-

hostname = '101.201.43.223'
username = 'aduser'
password = 'Jason0322%'
database = 'adshow'

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT * FROM appinfo limit 10" )

    for stored_id in cur.fetchall() :
        print stored_id


print "Using psycopg2…"
import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery( myConnection )
myConnection.close()

print "Using PyGreSQL…"
import pgdb
myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
doQuery( myConnection )
myConnection.close()
