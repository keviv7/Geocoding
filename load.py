import sqlite3

connection=sqlite3.connect('geoData.sqlite')
cursorObj=connection.cursor()

cursorObj.execute('select * from Locations')

fHandler=open('data.js','w')
fHandler.write('citiesData=[\n')

for row in cursorObj:
    line='['+str(row[0])+','+str(row[1])+','+str(row[2])+']'+','
    fHandler.write(line)

fHandler.write('];')
fHandler.close()
