import cv2
import numpy as np
from models import Frame
import uuid
import time

class Camera:
    """카메라 모듈"""
    
    def __init__(self):
        self.is_active = False
        self.cap = None
        
    def initialize_and_activate(self) -> bool:
        """카메라 초기화 및 활성화"""
        try:
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.is_active = True
                print("카메라가 성공적으로 초기화되었습니다.")
                return True
            else:
                print("카메라 초기화에 실패했습니다.")
                return False
        except Exception as e:
            print(f"카메라 초기화 오류: {e}")
            return False
    
    def get_frame(self) -> Optional[Frame]:
        """현재 프레임 제공"""
        if not self.is_active or not self.cap:
            return None
            
        ret, frame = self.cap.read()
        if ret:
            height, width = frame.shape[:2]
            _, buffer = cv2.imencode('.jpg', frame)
            
            return Frame(
                frame_id=str(uuid.uuid4()),
                image_data=buffer.tobytes(),
                timestamp=time.time(),
                width=width,
                height=height
            )
        return None
    
    def release(self):
        """카메라 리소스 해제"""
        if self.cap:
            self.cap.release()
        self.is_active = False