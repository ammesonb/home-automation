#!/usr/bin/python
import requests
import json
import psycopg2.extras
from automation import openDBConnection

hueKey = "B8xfnnoFBcq2apGNQJCKKtTCSTIwgShZ508owHCz"
hueAddr = 'http://hue-bridge-2.lan/api/{0}'.format(hueKey)

def refreshDB():
    dbConn = openDBConnection()
    dbCursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    lights = getLights()
    lkeys = lights.keys()
    groups = getGroups()
    gkeys = groups.keys()

    for l in lkeys:
        dbCursor.execute("SELECT EXISTS(SELECT 1 FROM lights WHERE id=%s)", [l])
        exists = dbCursor.fetchone()[0]
        if not exists:
            dbCursor.execute("INSERT INTO lights (id, name) VALUES (%s, %s)", [l, lights[l]['name']])
        else:
            dbCursor.execute("UPDATE lights SET name=%s WHERE id=%s)", [lights[l]['name'], l])

    for g in gkeys:
        dbCursor.execute("SELECT EXISTS(SELECT 1 FROM rooms WHERE id=%s)", [g])
        exists = dbCursor.fetchone()[0]
        if not exists:
            dbCursor.execute("INSERT INTO rooms (id, room) VALUES (%s, %s)", [g, groups[g]['name']])
        else:
            dbCursor.execute("UPDATE rooms SET room=%s WHERE id=%s)", [groups[g]['name'], g])
    
    dbConn.commit()

def getLights():
    r = requests.get(hueAddr + '/lights')
    return json.loads(r.content)

def getGroups():
    r = requests.get(hueAddr + '/groups')
    return json.loads(r.content)

def changePower(kind, ident, state):
    r = requests.put(hueAddr + '/{0}/{1}/state'.format(kind, ident), data=json.dumps({"on":state}))
    r = json.loads(r.content)[0]
    return r.has_key("success") and len(r['success']) > 0
