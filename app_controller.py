from typing import List, Optional
from models import Frame, Filter, MediaFile
from camera_module import Camera
from face_detector import FaceDetector
from filter_database import FilterDB
from ar_engine import AREngine
from media_manager import MediaManager
from network_manager import NetworkManager

class AppController:
    """앱 컨트롤러 - 전체 시스템 조율"""
    
    def __init__(self):
        self.camera = Camera()
        self.face_detector = FaceDetector()
        self.filter_db = FilterDB()
        self.ar_engine = AREngine()
        self.media_manager = MediaManager()
        self.network_manager = NetworkManager()
        self.current_filter = None
        self.is_camera_active = False
    
    def activate_camera(self) -> bool:
        """카메라 활성화"""
        success = self.camera.initialize_and_activate()
        if success:
            self.is_camera_active = True
            print("카메라가 활성화되었습니다.")
        return success
    
    def get_camera_feed(self) -> Optional[Frame]:
        """카메라 피드 제공"""
        if not self.is_camera_active:
            return None
        return self.camera.get_frame()
    
    def detect_faces(self, frame: Frame) -> List:
        """얼굴 인식 요청"""
        return self.face_detector.detect_faces(frame)
    
    def get_available_filters(self) -> List[Filter]:
        """사용 가능한 필터 목록 요청"""
        return self.filter_db.get_available_filters()
    
    def select_filter(self, filter_id: str) -> bool:
        """필터 선택"""
        filter_assets = self.filter_db.get_filter_assets(filter_id)
        if filter_assets:
            self.current_filter = filter_assets
            print(f"필터가 선택되었습니다: {filter_id}")
            return True
        return False
    
    def render_ar_frame(self, frame: Frame) -> Optional[Frame]:
        """AR 필터가 적용된 프레임 렌더링"""
        if not self.current_filter:
            return frame
        
        # 얼굴 인식
        face_infos = self.detect_faces(frame)
        
        if face_infos:
            # AR 필터 적용
            return self.ar_engine.render_filter(frame, face_infos, self.current_filter)
        
        return frame
    
    def capture_media(self, frame: Frame) -> MediaFile:
        """미디어 캡처"""
        return self.media_manager.capture_frame(frame)
    
    def upload_content(self, media_file: MediaFile, caption: str = "", 
                      hashtags: List[str] = None) -> dict:
        """콘텐츠 업로드"""
        metadata = {
            "caption": caption,
            "hashtags": hashtags or [],
            "filter_id": self.current_filter.get("filter_id") if self.current_filter else None,
            "timestamp": media_file.timestamp
        }
        
        return self.network_manager.upload_content(media_file, metadata)
    
    def cleanup(self):
        """리소스 정리"""
        self.camera.release()
        self.is_camera_active = False
        print("리소스가 정리되었습니다.")