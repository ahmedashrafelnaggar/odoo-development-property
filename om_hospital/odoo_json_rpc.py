import json
import random
import urllib.request

HOST = 'localhost'
PORT = 8069
DB = 'Hospital'
USER = 'admin'
PASS = 'admin'

def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type":"application/json",
    })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]

def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})

url = "http://%s:%s/jsonrpc" % (HOST, PORT)
print('url....', url)
uid = call(url, "common", "login", DB, USER, PASS)
# here will be output user .....2 this mean password is valid
print('uid....', uid)



# create method
# args = {
#
#     # this is name_field which called name i want this field this is his new name
#     'name': 'This note from json rpc',
#
# }
# # you write the name of model like 'hospital.patient'
# name = call(url, "object", "execute", DB, uid, PASS, 'hospital.patient', 'create', args)
# print('name is:', name)


# read method
# you write the name of model like 'hospital.patient'
# name = call(url, "object", "execute", DB, uid, PASS, 'hospital.patient', 'read', [id ] beta3 el model elly enta 3ayez read it ])
# model = call(url, "object", "execute", DB, uid, PASS, 'hospital.patient', 'read', [3])
# print('model is:', model)



# write/update using json_rpc

# vals = {
#     # this is name_field which called name i want this field this is his new name
#     'name': 'odoo mates'
# }
# # you write the name of model like 'hospital.patient'
# name = call(url, "object", "execute", DB, uid, PASS, 'hospital.doctor', 'write', [3], vals)
# # print(name)


# delete/unlink using json_rpc

# project_id = call(url, "object", "execute", DB, uid, PASS, "project.project", "unlink", [ids]) this ka3eda
name = call(url, "object", "execute", DB, uid, PASS, 'hospital.doctor', 'unlink', [2])




