from itsmodel import IntersightConnector

# Global Variables
api_key = '6553415a7564613305ea6a02/6553415a7564613305ea6a06/655627c0756461320535beb6'
api_key_file = './.intersight.pem'
api_endpoint = 'https://eu-central-1.intersight.com'

# Connect to Intersight
ic = IntersightConnector(api_key, api_key_file, api_endpoint)

# Use the Intersight Connector to make REST API Calls
res = ic.read('organization/Organization')
print('Listing organizations:')
for o in res:
    print(f' * {o.name}, {o.moid}')
print()

res = ic.create('organization/Organization', {'name': 'NewOrg_Create'})
moid = res.moid
print(f'created object: {res.name} {res.moid}')

res = ic.update('organization/Organization', moid, {'name': 'NewOrg_Update'})
print(f'updated object {res.name} {res.moid}')

ic.delete('organization/Organization', moid)
print(f'deleted object {res.name} {moid}')
