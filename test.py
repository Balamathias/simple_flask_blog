from urllib import request


# req = request.urlopen('http://localhost:5000/api/users')
# res = req.read().decode('utf-8')

# print(res)

# Write some code that posts a users register info with a post request to the endpoint above
import urllib.request

url = 'http://localhost:5000/api/users'

user_info = {
    'username': 'matie',
    'password': 'matie',
    'email': 'matie@gmail.com'
}

headers = {
    'Content-Type': 'Application/json'
}

req = urllib.request.Request(
    url=url,
    method='post',
    headers=headers,
    data=user_info
)


print(req.data)
