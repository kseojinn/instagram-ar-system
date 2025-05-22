from ui_simulator import UISimulator

def main():
    """메인 실행 함수"""
    print("Instagram AR Filter System 시작")
    
    # UI 시뮬레이터 실행
    ui = UISimulator()
    ui.start_camera_session()

if __name__ == "__main__":
    main()