import uuid
from datetime import datetime

class BaseModel:
    def __init__(self, *args, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_active = True

    def update(self):
        """Cập nhật thời gian chỉnh sửa mỗi khi dữ liệu thay đổi"""
        self.updated_at = datetime.now()

    def delete(self):
        """Xóa ảo: không xóa khỏi DB nhưng đánh dấu là ngừng hoạt động"""
        self.is_active = False
        self.update()

    def to_dict(self):
        """Chuyển đổi đối tượng sang dictionary (rất hữu ích khi lưu JSON hoặc trả về API)"""
        return {
            k: v.isoformat() if isinstance(v, datetime) else v
            for k, v in self.__dict__.items()
        }