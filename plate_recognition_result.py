from typing import List
from datetime import datetime


class Box:
    xmin: int
    ymin: int
    xmax: int
    ymax: int


class Candidate:
    score: float
    plate: str


class Region:
    code: str
    score: float


class Vehicle:
    score: float
    type: str
    box: Box


class Result:
    box: Box
    plate: str
    region: Region
    score: float
    candidates: List[Candidate]
    dscore: float
    vehicle: Vehicle


class PlateRecognitionResult:
    processing_time: float
    results: List[Result]
    filename: str
    version: int
    camera_id: None
    timestamp: datetime

    def __init__(self, in_dict: dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(self, key, [PlateRecognitionResult(x) if isinstance(x, dict) else x for x in val])
            else:
                setattr(self, key, PlateRecognitionResult(val) if isinstance(val, dict) else val)

    def is_plate_found(self):
        if self.results:
            return True
        return False
