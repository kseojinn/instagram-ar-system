import cv2
import numpy as np
from typing import List, Optional
from models import Frame, FaceInfo, FaceLandmark
import uuid

class FaceDetector:
    """얼굴 인식 모듈"""
    
    def __init__(self):
        # OpenCV의 하르 캐스케이드 분류기 사용
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        # 눈 검출기 (랜드마크 시뮬레이션용)
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
    
    def detect_faces(self, frame: Frame) -> List[FaceInfo]:
        """얼굴 인식 및 특징점 감지"""
        # 바이트 데이터를 OpenCV 이미지로 변환
        nparr = np.frombuffer(frame.image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 얼굴 검출
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        
        face_infos = []
        for (x, y, w, h) in faces:
            # 간단한 랜드마크 시뮬레이션 (실제로는 더 정교한 알고리즘 사용)
            landmarks = self._generate_landmarks(x, y, w, h, gray)
            
            face_info = FaceInfo(
                face_id=str(uuid.uuid4()),
                bounding_box=(float(x), float(y), float(w), float(h)),
                landmarks=landmarks,
                confidence=0.95  # 시뮬레이션 값
            )
            face_infos.append(face_info)
        
        return face_infos
    
    def _generate_landmarks(self, x: int, y: int, w: int, h: int, 
                          gray_img: np.ndarray) -> List[FaceLandmark]:
        """얼굴 특징점 생성 (시뮬레이션)"""
        landmarks = []
        
        # 얼굴 영역에서 눈 검출
        roi_gray = gray_img[y:y+h, x:x+w]
        eyes = self.eye_cascade.detectMultiScale(roi_gray)
        
        # 주요 특징점들 시뮬레이션
        # 실제로는 68개 또는 478개의 정밀한 특징점을 사용
        key_points = [
            (x + w//4, y + h//3),      # 왼쪽 눈
            (x + 3*w//4, y + h//3),    # 오른쪽 눈
            (x + w//2, y + 2*h//3),    # 코
            (x + w//3, y + 4*h//5),    # 입 왼쪽
            (x + 2*w//3, y + 4*h//5),  # 입 오른쪽
        ]
        
        for px, py in key_points:
            landmarks.append(FaceLandmark(
                x=float(px),
                y=float(py),
                confidence=0.9
            ))
        
        return landmarks