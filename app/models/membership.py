from datetime import datetime, timedelta
from app.models.base import BaseModel


class MembershipPlan(BaseModel):
    """Gói tập (VD: 1 tháng, 6 tháng, 1 năm)"""

    def __init__(self, name, duration_days, price, description=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name                    # VD: "Gói 1 tháng", "Gói 6 tháng"
        self.duration_days = duration_days  # Số ngày của gói
        self.price = price                  # Giá gói (VND)
        self.description = description      # Mô tả thêm (tùy chọn)

    def __str__(self):
        return f"MembershipPlan(name={self.name}, duration={self.duration_days} ngày, price={self.price:,}đ)"


class MembershipSubscription(BaseModel):
    """Đăng ký gói tập của một hội viên"""

    STATUS_ACTIVE = "active"
    STATUS_EXPIRED = "expired"
    STATUS_CANCELLED = "cancelled"

    def __init__(self, member_id, plan_id, duration_days, price_paid, start_date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.member_id = member_id
        self.plan_id = plan_id
        self.price_paid = price_paid                        # Giá thực tế đã thanh toán
        self.start_date = start_date or datetime.now()
        self.end_date = self.start_date + timedelta(days=duration_days)
        self.status = self.STATUS_ACTIVE

    def is_expired(self):
        """Kiểm tra gói tập đã hết hạn chưa"""
        return datetime.now() > self.end_date

    def days_remaining(self):
        """Số ngày còn lại của gói tập"""
        remaining = (self.end_date - datetime.now()).days
        return max(remaining, 0)

    def cancel(self):
        """Hủy gói tập"""
        self.status = self.STATUS_CANCELLED
        self.update()

    def refresh_status(self):
        """Cập nhật trạng thái nếu gói đã hết hạn"""
        if self.status == self.STATUS_ACTIVE and self.is_expired():
            self.status = self.STATUS_EXPIRED
            self.update()

    def __str__(self):
        return (f"MembershipSubscription(member_id={self.member_id}, "
                f"status={self.status}, end_date={self.end_date.strftime('%d/%m/%Y')})")
