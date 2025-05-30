import http.client

connection = http.client.HTTPSConnection("www.its.ac.id")
connection.request("GET", "/")
response = connection.getresponse()
# header = response.getheaders()
# convert headers to dictionary
headers = dict(response.getheaders())
#Get the actual body of the response
print("Response:",response.read())
print("Status", response.status, response.reason)
print("Server:", headers.get("Server"))
# print("Response header:")
# for item in header:
#     print(item)



