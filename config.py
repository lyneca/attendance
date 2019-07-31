from logger import *

class Config:
    def __init__(self, bot_id):
        self.bot_id = 0
        self.server = ""
        self.course_id = ""
        self.access_token = ""

    def update_config(self):
        # TODO Get data from Firebase; encrypted?
        return True
