from os import listdir
from os.path import isfile, join
import json
from datetime import datetime

from settings import *

class Users:
    print(f"[i] ({datetime.now().strftime(TIME_FORMAT)}) Users init complete")

    @staticmethod
    def get_data(user, variable, empty_variable=None):
        users = [f[:-len(USER_FILE_TYPE)] for f in listdir(USERS_FOLDER) if isfile(join(USERS_FOLDER, f))]
        if not user in users:
            return empty_variable
        
        with open(join(USERS_FOLDER, f"{user}{USER_FILE_TYPE}")) as f:
            data = json.loads(f.read())

        if not variable in data or data[variable] is None:
            return empty_variable

        return data[variable]

    @staticmethod
    def send_data(user, data):
        users = [f[:-len(USER_FILE_TYPE)] for f in listdir(USERS_FOLDER) if isfile(join(USERS_FOLDER, f))]
        if user in users:
            with open(join(USERS_FOLDER, f"{user}{USER_FILE_TYPE}")) as f:
                old_data = json.loads(f.read())
        else:
            old_data = {}

        for variable in data:
            old_data[variable] = data[variable]

        with open(join(USERS_FOLDER, f"{user}{USER_FILE_TYPE}"), "w") as f:
            f.write(json.dumps(old_data))

    @staticmethod
    def get_data_from_all_users(variable, empty_variable=None):
        users = [f[:-len(USER_FILE_TYPE)] for f in listdir(USERS_FOLDER) if isfile(join(USERS_FOLDER, f))]
        data = {}

        for user in users:
            with open(join(USERS_FOLDER, f"{user}{USER_FILE_TYPE}")) as f:
                current_data = json.loads(f.read())
            if not variable in current_data or current_data[variable] is None:
                data[user] = empty_variable
            else:
                data[user] = current_data[variable]
        
        return data