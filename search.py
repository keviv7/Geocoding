from urllib import request,parse
import json
import sqlite3
import time

connection=sqlite3.connect('geoData.sqlite')
cursorObj=connection.cursor()

cursorObj.execute('''
create table if not exists Locations(city text, latitue decimal,longitude decimal);
''')

#using nominatin geocoding api
serviceUrl='https://nominatim.openstreetmap.org/search?'

fHandler=open('cities.txt','r')

for city in fHandler:

    cursorObj.execute('''
    select city from Locations where city=?
    ''',(city,))

    # don't request if data is there in database
    if(cursorObj.fetchone()!=None): continue

    parms=dict()
    resultFormat='json'
    parms['city']=city
    parms['format']=resultFormat

    url=serviceUrl+parse.urlencode(parms)
    httpResponse=request.urlopen(url)
    byteData=httpResponse.read()
    stringData=byteData.decode()

    data=json.loads(stringData)

    if(len(data)<1): continue

    latitude=data[0]['lat']
    longitude=data[0]['lon']

    cursorObj.execute('''
    insert into Locations(city,latitue,longitude) values(?,?,?)
    ''',(city,latitude,longitude,))

    connection.commit()

    print(city+' retrieved and stored in database..')

    #usage policy of the api allows maximum 1 request/sec
    time.sleep(1)

fHandler.close()

