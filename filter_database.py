from typing import List, Optional
from models import Filter, FilterType

class FilterDB:
    """필터 데이터베이스"""
    
    def __init__(self):
        self.filters = self._initialize_filters()
    
    def _initialize_filters(self) -> List[Filter]:
        """필터 목록 초기화"""
        return [
            Filter(
                filter_id="filter_001",
                name="강아지 귀",
                filter_type=FilterType.ANIMAL,
                asset_path="/assets/filters/dog_ears.json",
                thumbnail_path="/assets/thumbnails/dog_ears.jpg",
                description="귀여운 강아지 귀 필터"
            ),
            Filter(
                filter_id="filter_002",
                name="빈티지 필름",
                filter_type=FilterType.VINTAGE,
                asset_path="/assets/filters/vintage_film.json",
                thumbnail_path="/assets/thumbnails/vintage_film.jpg",
                description="레트로 감성 빈티지 필터"
            ),
            Filter(
                filter_id="filter_003",
                name="뷰티 보정",
                filter_type=FilterType.BEAUTY,
                asset_path="/assets/filters/beauty_enhance.json",
                thumbnail_path="/assets/thumbnails/beauty_enhance.jpg",
                description="자연스러운 뷰티 보정 필터"
            ),
            Filter(
                filter_id="filter_004",
                name="무지개 안경",
                filter_type=FilterType.FUNNY,
                asset_path="/assets/filters/rainbow_glasses.json",
                thumbnail_path="/assets/thumbnails/rainbow_glasses.jpg",
                description="재미있는 무지개 안경 필터"
            )
        ]
    
    def get_available_filters(self) -> List[Filter]:
        """사용 가능한 필터 목록 반환"""
        return self.filters.copy()
    
    def get_filter_by_id(self, filter_id: str) -> Optional[Filter]:
        """ID로 필터 검색"""
        for filter_obj in self.filters:
            if filter_obj.filter_id == filter_id:
                return filter_obj
        return None
    
    def get_filter_assets(self, filter_id: str) -> Optional[dict]:
        """필터 에셋 및 설정 반환"""
        filter_obj = self.get_filter_by_id(filter_id)
        if filter_obj:
            # 실제로는 파일에서 로드
            return {
                "filter_id": filter_obj.filter_id,
                "assets": {
                    "textures": [f"{filter_obj.asset_path}/texture.png"],
                    "models": [f"{filter_obj.asset_path}/model.obj"],
                    "shaders": [f"{filter_obj.asset_path}/shader.glsl"]
                },
                "settings": {
                    "opacity": 0.8,
                    "scale": 1.0,
                    "position_offset": {"x": 0, "y": -20}
                }
            }
        return None