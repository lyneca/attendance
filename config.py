from logger import *

class Config:
    def __init__(self):
        with open("/home/pi/id") as id_file:
            self.bot_id = int(id_file.read())
        self.server = ""
        self.course_id = ""
        self.access_token = ""

    def update_config(self):
        # TODO Get data from Firebase; encrypted?
        return True
