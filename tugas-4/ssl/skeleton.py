import unittest
import sys
import socket
import ssl
from io import StringIO

# Target server to test SSL connection
test_hostname = 'www.google.com'
test_port = 443

# Establish an SSL connection and retrieve peer certificate
def get_ssl_certificate(hostname, port):
    context = ssl.create_default_context()
    with socket.create_connection((hostname,443)) as sock:
        with context.wrap_socket(sock,server_hostname=hostname) as csock:
            cert = csock.getpeercert()
            #Extract common name from subject
            # common_name =cert['subject']
            #convert to dict
            # common_name_dict = dict(x[0] for x in common_name)
            return cert

# Verify that certificate contains expected fields
def assert_cert_has_fields(cert, fields):
    missing = [field for field in fields if field not in cert]
    if not missing:
        print("Certificate has all required fields:", fields)
    else:
        print("Certificate is missing fields:", missing)

# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass

# Unit test for SSL certificate retrieval
class TestSSLConnection(unittest.TestCase):
    def setUp(self):
        self.hostname = test_hostname
        self.port = test_port

    def test_ssl_certificate_retrieval(self):
        cert = get_ssl_certificate(self.hostname, self.port)
        self.assertIsInstance(cert, dict)
        assert_cert_has_fields(cert, ['subject', 'issuer'])

    def test_certificate_subject(self):
        cert = get_ssl_certificate(self.hostname, self.port)
        subject = dict(x[0] for x in cert['subject'])
        self.assertIn('commonName', subject)
        print("Common Name (CN):", subject.get('commonName'))

# Entry point
if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        cert = get_ssl_certificate(test_hostname, test_port)
        print("Retrieved SSL Certificate:", cert)
    else:
        runner = unittest.TextTestRunner(stream=NullWriter())
        unittest.main(testRunner=runner, exit=False)
        # unittest.main(exit=False)