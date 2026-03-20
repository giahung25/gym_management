import os

# Đường dẫn gốc dự án (thư mục chứa app/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.path.join(BASE_DIR, "data", "gym_db.db")

APP_TITLE = "GymAdmin Management System"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
