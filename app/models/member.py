# ============================================================================
# FILE: app/models/member.py
# MỤC ĐÍCH: Định nghĩa class Member — đại diện cho một HỘI VIÊN phòng gym.
#            Kế thừa từ BaseModel → tự động có id, created_at, updated_at, is_active.
#
# KIẾN THỨC:
#   - Kế thừa: class Member(BaseModel) nghĩa là Member "con" của BaseModel
#   - super().__init__() = gọi hàm __init__ của class cha (BaseModel)
#   - Mỗi Member object đại diện cho 1 dòng (row) trong bảng `members` của database
# ============================================================================

from app.models.base import BaseModel  # Import class cha


class Member(BaseModel):
    """Đại diện cho một hội viên phòng gym.

    Thuộc tính (từ BaseModel): id, created_at, updated_at, is_active
    Thuộc tính riêng: name, phone, email, gender, date_of_birth, address, emergency_contact, photo
    """

    def __init__(self, name, phone, email=None, gender=None,
                 date_of_birth=None, address=None, emergency_contact=None,
                 photo=None, *args, **kwargs):
        """Khởi tạo một hội viên mới.

        Tham số:
            name (str):              Họ tên hội viên — BẮT BUỘC
            phone (str):             Số điện thoại — BẮT BUỘC
            email (str, optional):   Email — tùy chọn (mặc định None = không có)
            gender (str, optional):  Giới tính: 'male' | 'female' | 'other'
            date_of_birth (str/date, optional): Ngày sinh
            address (str, optional): Địa chỉ
            emergency_contact (str, optional): Số điện thoại liên hệ khẩn cấp
            photo (str, optional):   Đường dẫn file ảnh đại diện

        VD tạo hội viên:
            member = Member(name="Nguyễn Văn A", phone="0901234567", email="a@gmail.com")
        """
        # Gọi __init__ của BaseModel (class cha) để tạo id, created_at, updated_at, is_active
        super().__init__(*args, **kwargs)

        # Gán các thuộc tính riêng của Member
        self.name = name                            # Họ tên (VD: "Nguyễn Văn A")
        self.phone = phone                          # Số điện thoại (VD: "0901234567")
        self.email = email                          # Email (VD: "a@gmail.com" hoặc None)
        self.gender = gender                        # Giới tính: 'male' | 'female' | 'other'
        self.date_of_birth = date_of_birth          # Ngày sinh (VD: "2000-01-15")
        self.address = address                      # Địa chỉ nhà
        self.emergency_contact = emergency_contact  # SĐT liên hệ khẩn cấp
        self.photo = photo                          # Đường dẫn ảnh (VD: "photos/avatar1.jpg")

    def __str__(self):
        """Hàm đặc biệt: khi print(member) → Python gọi __str__() để lấy chuỗi hiển thị.

        VD: print(member)
            → "Member(id=abc123, name=Nguyễn Văn A, phone=0901234567)"
        """
        return f"Member(id={self.id}, name={self.name}, phone={self.phone})"
