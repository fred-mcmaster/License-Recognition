from typing import List
from datetime import datetime

class Box:
    xmin: int
    ymin: int
    xmax: int
    ymax: int

    def __init__(self, xmin: int, ymin: int, xmax: int, ymax: int) -> None:
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax


class Candidate:
    score: float
    plate: str

    def __init__(self, score: float, plate: str) -> None:
        self.score = score
        self.plate = plate


class Region:
    code: str
    score: float

    def __init__(self, code: str, score: float) -> None:
        self.code = code
        self.score = score


class Vehicle:
    score: float
    type: str
    box: Box

    def __init__(self, score: float, type: str, box: Box) -> None:
        self.score = score
        self.type = type
        self.box = box


class Result:
    box: Box
    plate: str
    region: Region
    score: float
    candidates: List[Candidate]
    dscore: float
    vehicle: Vehicle

    def __init__(self, box: Box, plate: str, region: Region, score: float, candidates: List[Candidate], dscore: float, vehicle: Vehicle) -> None:
        self.box = box
        self.plate = plate
        self.region = region
        self.score = score
        self.candidates = candidates
        self.dscore = dscore
        self.vehicle = vehicle


class PlateRecognitionResult:
    processing_time: float
    results: List[Result]
    filename: str
    version: int
    camera_id: None
    timestamp: datetime

    def __init__(self, processing_time: float, results: List[Result], filename: str, version: int, camera_id: None, timestamp: datetime) -> None:
        self.processing_time = processing_time
        self.results = results
        self.filename = filename
        self.version = version
        self.camera_id = camera_id
        self.timestamp = timestamp

    def is_plate_found(self):
        if self.results:
            return True
        return False
