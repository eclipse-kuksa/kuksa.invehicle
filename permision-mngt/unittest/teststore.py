import unittest
import tokenStore


class TestKeystoreMethods(unittest.TestCase):
    def test_store(self):
        dummy_token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzd3BPeXZVUGZLc0lhbmhlT0xvQUVyTG4wTDNBOVNLa0pJVXk2aFc4UTd3In0.eyJqdGkiOiI3ZmE2ZDcyOS0xMDUxLTQ1MTMtYWNkNy0wYjNmMGRhOWYwMDAiLCJleHAiOjE1Njc1NTcyOTgsIm5iZiI6MCwiaWF0IjoxNTY3NTIxMjk4LCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODAvYXV0aC9yZWFsbXMvS3Vrc2EiLCJzdWIiOiI4MjA3ZTU5MC1iZjg2LTQ1OWMtOTZkZC0yNGVkYTZmZWRlZDAiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJLdWtzYS1kYXNoYm9hcmQiLCJhdXRoX3RpbWUiOjAsInNlc3Npb25fc3RhdGUiOiIxNzk3MDMzYS1hNTc1LTRmMTItYWE3NS05NDA1NmU5OTFlNWIiLCJhY3IiOiIxIiwic2NvcGUiOiIiLCJjbGllbnRJZCI6Ikt1a3NhLWRhc2hib2FyZCIsImNsaWVudEhvc3QiOiIxMjcuMC4wLjEiLCJ3M2MtdnNzIjp7IlNpZ25hbC5PQkQuUlBNIjoiciJ9LCJjbGllbnRBZGRyZXNzIjoiMTI3LjAuMC4xIn0.KrfmmC-2WsY-FnDmzeitj1PKG4oWiPKghWqy7RPH5QF-z9C-iQ75IQnxo4JAJCZBsbhdjUnsbtRSuk6MvzUsbiACcB09FRMJkS5vxoxjnR3dJu0Ux2iZsVVRcluJFHLq6m2ZzESZGEPd-r--LKIrFQTpqJ2h9CiusXOXx2XPxU14Y2hSA9tTdhpULB5JehBNJ2TQzMo0KPmpGgv0GdNSmq5QM8TZGT5xzFrIoT8KvkwtFI2uStnTD-E8Spb5v9uPK_upn8DreTVSXUzzahMInolKUD7GLJY1UZPQrKnor9znYby8NQgAC11JaKB3rleBtOhJPO_-d8UVn0FopznXLg'
        appID = "Kuksa-dashboard"
        api = "w3c-vss"
        tokenStore.storeToken(appID, api, dummy_token)
        token = tokenStore.getToken(appID, api)
        assert (dummy_token == token)


if __name__ == '__main__':
    unittest.main()
