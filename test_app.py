import unittest
from app import *
from users import *
from devices import *

# Unit test format based on: https://www.youtube.com/watch?v=6tNS--WetLI&ab_channel=CoreySchafer

class TestmedAPI(unittest.TestCase):

    def test_patientPost(self):
        correctTest = [11111,"Timmy Test","TestHospital",11,111,11,111,11,111,11]

        users.post("http://127.0.0.1:5000/patients?patientID=11111&name=Timmy Test&hospital=TestHospital&temperature=11&systolicBP=111&diastolicBP=11&pulse=111&oximeter=11&weight=111&glucometer=11")
        response = users.get("http://127.0.0.1:5000/patients?patientID=12340")

        self.assertDictEqual(response, correctTest)


if __name__ == "__main__":
    unittest.main()