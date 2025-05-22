import time
from typing import List, Optional
from app_controller import AppController
from models import Filter, MediaFile

class UISimulator:
    """사용자 인터페이스 시뮬레이터"""
    
    def __init__(self):
        self.app_controller = AppController()
        self.current_frame = None
        self.captured_media = None
    
    def start_camera_session(self):
        """카메라 세션 시작"""
        print("\n=== Instagram AR 카메라 세션 시작 ===")
        
        # 1. 카메라 활성화
        if not self.app_controller.activate_camera():
            print("카메라 활성화 실패")
            return
        
        # 2. 필터 목록 표시
        self._display_filter_list()
        
        # 3. 사용자 상호작용 시뮬레이션
        self._simulate_user_interaction()
    
    def _display_filter_list(self):
        """필터 목록 표시"""
        filters = self.app_controller.get_available_filters()
        print("\n📱 사용 가능한 필터:")
        for i, filter_obj in enumerate(filters, 1):
            print(f"{i}. {filter_obj.name} ({filter_obj.filter_type.value})")
            print(f"   {filter_obj.description}")
        print("0. 필터 없음")
    
    def _simulate_user_interaction(self):
        """사용자 상호작용 시뮬레이션"""
        filters = self.app_controller.get_available_filters()
        
        # 필터 선택 시뮬레이션
        selected_filter_index = 1  # 강아지 귀 필터 선택
        if selected_filter_index > 0:
            selected_filter = filters[selected_filter_index - 1]
            self.app_controller.select_filter(selected_filter.filter_id)
            print(f"\n✅ '{selected_filter.name}' 필터가 선택되었습니다.")
        
        # 카메라 피드 및 AR 렌더링 시뮬레이션
        print("\n📹 카메라 피드 시작...")
        for i in range(3):  # 3프레임 처리
            frame = self.app_controller.get_camera_feed()
            if frame:
                # AR 필터 적용
                rendered_frame = self.app_controller.render_ar_frame(frame)
                self.current_frame = rendered_frame
                print(f"프레임 {i+1} 처리 완료 - AR 필터 적용됨")
                time.sleep(1)
        
        # 캡처 시뮬레이션
        if self.current_frame:
            print("\n📸 사진 캡처...")
            self.captured_media = self.app_controller.capture_media(self.current_frame)
            print(f"✅ 캡처 완료: {self.captured_media.file_path}")
        
        # 업로드 시뮬레이션
        if self.captured_media:
            print("\n📤 Instagram에 게시...")
            upload_result = self.app_controller.upload_content(
                self.captured_media,
                caption="AR 필터로 찍은 재미있는 사진! 🐶",
                hashtags=["#AR", "#Instagram", "#Filter", "#Selfie"]
            )
            
            if upload_result["success"]:
                print(f"✅ 게시 완료!")
                print(f"포스트 ID: {upload_result['post_id']}")
                print(f"URL: {upload_result['url']}")
            else:
                print("❌ 게시 실패")
        
        # 정리
        self.app_controller.cleanup()
        print("\n=== 세션 종료 ===")


# main.py - 메인 실행 파일
def main():
    """메인 실행 함수"""
    print("Instagram AR Filter System 시작")
    
    # UI 시뮬레이터 실행
    ui = UISimulator()
    ui.start_camera_session()

if __name__ == "__main__":
    main()