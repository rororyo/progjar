import http.client
import gzip
from io import BytesIO

# Make HTTPS request
connection = http.client.HTTPSConnection("www.its.ac.id")
connection.request("GET", "/")
response = connection.getresponse()

# Get headers
headers = dict(response.getheaders())

# Read body as bytes
body = response.read()

# Check if the content is compressed
if headers.get("Content-Encoding") == "gzip":
    buf = BytesIO(body)
    f = gzip.GzipFile(fileobj=buf)
    body = f.read()

# Decode from bytes to string (assume utf-8 unless header says otherwise)
charset = "utf-8"
content_type = headers.get("Content-Type", "")
if "charset=" in content_type:
    charset = content_type.split("charset=")[-1]

text = body.decode(charset, errors="replace")
print(text)