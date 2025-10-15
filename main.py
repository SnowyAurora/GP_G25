from gui.main_dashboard import launch
from app.admin_utils import backup_data, init_logger

if __name__ == "__main__":
    init_logger()
    backup_data()
    launch()