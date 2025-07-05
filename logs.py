from datetime import datetime
from settings import *

class Logs():
    def print_log(type, message):
        print(f"[{type}] ({datetime.now().strftime(TIME_FORMAT)}) {message}")