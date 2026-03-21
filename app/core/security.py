from app.core.config import ADMIN_USERNAME, ADMIN_PASSWORD


def check_login(username: str, password: str) -> bool:
    """Kiểm tra thông tin đăng nhập. Trả về True nếu hợp lệ."""
    return username.strip() == ADMIN_USERNAME and password == ADMIN_PASSWORD
