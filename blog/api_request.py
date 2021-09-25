import requests
import pprint

# response = requests.get('http://127.0.0.1:8000/api/v0/tags/', auth=('author', 'dante123456'))
#
# pprint.pprint(response.json())

token = '15549b9bfc64dbb1008048534562d5ee4bd74dde'
headers = {'Authorization': f'Token {token}'}
response = requests.get('http://127.0.0.1:8000/api/v0/tags/', headers=headers)
# response = requests.get('http://127.0.0.1:8000/api/v0/tags/')
pprint.pprint(response.json())
