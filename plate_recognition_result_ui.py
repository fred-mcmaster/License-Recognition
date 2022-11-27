import json


class Plate:
    number: str
    score: str

    def __init__(self, number: str, score: str):
        self.number = number
        self.score = score


class Region:
    name: str
    score: str

    def __init__(self, name: str, score: str):
        self.name = name
        self.score = score


class Vehicle:
    type: str
    score: str

    def __init__(self, type: str, score: str):
        self.type = type
        self.score = score


class PlateRecognitionUiResults:
    plate: Plate
    region: Region
    vehicle: Vehicle

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
