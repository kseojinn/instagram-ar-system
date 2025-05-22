from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum
import time

class FilterType(Enum):
    BEAUTY = "beauty"
    ANIMAL = "animal"
    VINTAGE = "vintage"
    FUNNY = "funny"

@dataclass
class FaceLandmark:
    """얼굴 특징점 정보"""
    x: float
    y: float
    confidence: float

@dataclass
class FaceInfo:
    """얼굴 인식 결과"""
    face_id: str
    bounding_box: Tuple[float, float, float, float]  # x, y, width, height
    landmarks: List[FaceLandmark]
    confidence: float

@dataclass
class Filter:
    """AR 필터 정보"""
    filter_id: str
    name: str
    filter_type: FilterType
    asset_path: str
    thumbnail_path: str
    description: str

@dataclass
class MediaFile:
    """미디어 파일 정보"""
    file_id: str
    file_path: str
    file_type: str  # "image" or "video"
    size: int
    timestamp: float

@dataclass
class Frame:
    """카메라 프레임 데이터"""
    frame_id: str
    image_data: bytes
    timestamp: float
    width: int
    height: int