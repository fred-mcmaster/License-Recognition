import requests
import json

from plate_recognition_result import PlateRecognitionResult

API_KEY = "b043ef3a2da24bbde85109c5b49b61046519a1bc"

def identify_license_plate_from_image(encodedImage):
    data = dict(regions="", config={}, upload=encodedImage)
    _session = requests.Session()
    _session.headers.update({'Authorization': 'Token ' + API_KEY})
    response = _session.post('https://api.platerecognizer.com/v1/plate-reader/', data=data)

    jsonData = json.loads(response.text)
    resultData = PlateRecognitionResult(jsonData)
    return resultData
