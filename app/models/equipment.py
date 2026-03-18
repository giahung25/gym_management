from datetime import datetime
from app.models.base import BaseModel


class Equipment(BaseModel):
    """Thiết bị / máy móc trong phòng gym"""

    STATUS_WORKING = "working"          # Hoạt động tốt
    STATUS_BROKEN = "broken"            # Đang hỏng
    STATUS_MAINTENANCE = "maintenance"  # Đang bảo trì

    def __init__(self, name, category, quantity=1,
                 purchase_date=None, notes=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name                            # Tên thiết bị (VD: "Máy chạy bộ")
        self.category = category                    # Loại (VD: "Cardio", "Tạ tự do", "Máy lực")
        self.quantity = quantity                    # Số lượng
        self.status = self.STATUS_WORKING           # Trạng thái ban đầu
        self.purchase_date = purchase_date          # Ngày mua (datetime.date)
        self.notes = notes                          # Ghi chú thêm

    def mark_broken(self, notes=None):
        """Đánh dấu thiết bị bị hỏng"""
        self.status = self.STATUS_BROKEN
        if notes:
            self.notes = notes
        self.update()

    def mark_maintenance(self, notes=None):
        """Đưa thiết bị vào bảo trì"""
        self.status = self.STATUS_MAINTENANCE
        if notes:
            self.notes = notes
        self.update()

    def mark_working(self):
        """Đánh dấu thiết bị hoạt động trở lại"""
        self.status = self.STATUS_WORKING
        self.update()

    def is_available(self):
        """Kiểm tra thiết bị có đang hoạt động không"""
        return self.status == self.STATUS_WORKING

    def __str__(self):
        return (f"Equipment(name={self.name}, category={self.category}, "
                f"quantity={self.quantity}, status={self.status})")
