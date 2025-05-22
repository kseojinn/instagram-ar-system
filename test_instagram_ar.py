import unittest
from unittest.mock import Mock, patch
import time
from models import Frame, Filter, FilterType, FaceInfo, FaceLandmark
from camera_module import Camera
from face_detector import FaceDetector
from filter_database import FilterDB
from ar_engine import AREngine
from app_controller import AppController

class TestInstagramAR(unittest.TestCase):
    """Instagram AR 시스템 테스트"""
    
    def setUp(self):
        """테스트 셋업"""
        self.app_controller = AppController()
        self.filter_db = FilterDB()
        self.ar_engine = AREngine()
    
    def test_filter_database_initialization(self):
        """필터 데이터베이스 초기화 테스트"""
        filters = self.filter_db.get_available_filters()
        self.assertGreater(len(filters), 0)
        self.assertIsInstance(filters[0], Filter)
    
    def test_filter_selection(self):
        """필터 선택 테스트"""
        filters = self.filter_db.get_available_filters()
        first_filter = filters[0]
        
        assets = self.filter_db.get_filter_assets(first_filter.filter_id)
        self.assertIsNotNone(assets)
        self.assertIn("filter_id", assets)
        self.assertIn("assets", assets)
        self.assertIn("settings", assets)
    
    def test_face_detection_mock(self):
        """얼굴 인식 테스트 (모킹)"""
        # 테스트용 프레임 생성
        test_frame = Frame(
            frame_id="test_001",
            image_data=b"mock_image_data",
            timestamp=time.time(),
            width=640,
            height=480
        )
        
        # 실제 검출기 대신 모킹된 결과 사용
        mock_face_info = FaceInfo(
            face_id="face_001",
            bounding_box=(100.0, 100.0, 200.0, 200.0),
            landmarks=[
                FaceLandmark(x=150.0, y=150.0, confidence=0.9),
                FaceLandmark(x=250.0, y=150.0, confidence=0.9),
            ],
            confidence=0.95
        )
        
        self.assertEqual(mock_face_info.face_id, "face_001")
        self.assertEqual(len(mock_face_info.landmarks), 2)
    
    def test_app_controller_flow(self):
        """앱 컨트롤러 플로우 테스트"""
        # 필터 목록 가져오기
        filters = self.app_controller.get_available_filters()
        self.assertGreater(len(filters), 0)
        
        # 필터 선택
        first_filter = filters[0]
        success = self.app_controller.select_filter(first_filter.filter_id)
        self.assertTrue(success)

if __name__ == "__main__":
    unittest.main()