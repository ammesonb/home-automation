#!/usr/bin/python
import requests
import json

hueKey = "B8xfnnoFBcq2apGNQJCKKtTCSTIwgShZ508owHCz"
hueAddr = 'http://hue-bridge-2.lan/api/{0}'.format(hueKey)

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
