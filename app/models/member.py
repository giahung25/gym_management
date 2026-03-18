from app.models.base import BaseModel

class Member(BaseModel):
    def __init__(self, name, phone, email=None, gender=None,
                 date_of_birth=None, address=None, emergency_contact=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.phone = phone
        self.email = email
        self.gender = gender                        # 'male' | 'female' | 'other'
        self.date_of_birth = date_of_birth          # datetime.date
        self.address = address
        self.emergency_contact = emergency_contact  # số điện thoại liên hệ khẩn cấp

    def __str__(self):
        return f"Member(id={self.id}, name={self.name}, phone={self.phone})"
