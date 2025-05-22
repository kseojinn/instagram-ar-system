import os
import uuid
import time
from typing import Optional
from models import Frame, MediaFile

class MediaManager:
    """미디어 관리자"""
    
    def __init__(self, storage_path: str = "./captured_media"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
    
    def capture_frame(self, frame: Frame) -> MediaFile:
        """현재 프레임 캡처"""
        file_id = str(uuid.uuid4())
        timestamp = time.time()
        file_name = f"capture_{int(timestamp)}_{file_id[:8]}.jpg"
        file_path = os.path.join(self.storage_path, file_name)
        
        # 프레임 데이터를 파일로 저장
        with open(file_path, 'wb') as f:
            f.write(frame.image_data)
        
        # 파일 크기 계산
        file_size = len(frame.image_data)
        
        return MediaFile(
            file_id=file_id,
            file_path=file_path,
            file_type="image",
            size=file_size,
            timestamp=timestamp
        )
    
    def get_media_info(self, file_id: str) -> Optional[MediaFile]:
        """미디어 파일 정보 조회"""
        # 실제 구현에서는 데이터베이스에서 조회
        for file in os.listdir(self.storage_path):
            if file_id in file:
                file_path = os.path.join(self.storage_path, file)
                return MediaFile(
                    file_id=file_id,
                    file_path=file_path,
                    file_type="image",
                    size=os.path.getsize(file_path),
                    timestamp=os.path.getmtime(file_path)
                )
        return None