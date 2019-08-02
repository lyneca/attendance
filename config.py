import logger
import requests

class Config:
    def __init__(self):
        with open("/home/pi/id") as id_file:
            self.bot_id = int(id_file.read())
        self.server = ""
        self.course_id = ""
        self.access_token = ""

    def update_config(self):
        """Pull config data from Firebase"""
        logger.info("Pulling config from Firebase")
        requests.post(
            "https://us-central1-usyd-attendance.cloudfunctions.net/getConfig",
            { "bot_id": self.bot_id }
        )
        return True
