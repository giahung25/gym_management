import os

# Đường dẫn gốc dự án (thư mục chứa app/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.path.join(BASE_DIR, "data", "gym_db.db")

APP_TITLE = "GymAdmin Management System"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

# Thông tin đăng nhập mặc định (có thể override qua biến môi trường)
ADMIN_USERNAME = os.environ.get("GYM_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("GYM_PASSWORD", "admin123")
