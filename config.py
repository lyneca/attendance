import requests
import json
import os

class Config:
    def __init__(self, logger):
        with open("/home/pi/id") as id_file:
            self.bot_id = int(id_file.read())
        with open("/home/pi/secret") as secret_file:
            self.firebase_secret = secret_file.read().strip()
        self.logger = logger
        self.ready = False
        self.server = "https://canvas.sydney.edu.au/api/v1"
        self.course_name = ""
        self.course_id = ""
        self.access_token = ""

    def __repr__(self):
        return f"<Config ({self.course_name},{self.course_id},{self.access_token})>"

    def save(self):
        """This method may not be used, as it's better to force staff to scan
        every time than mark people as attending for the wrong course"""

        if not os.path.exists('/home/pi/config.json'):
            open('/home/pi/config.json', 'x').close()
        with open('/home/pi/config.json', 'w') as f:
            json.dump({
                'course_name': self.course_name,
                'course_id': self.course_id,
                'token': self.access_token
            }, f)

    def update_config(self):
        """Pull config data from Firebase"""
        self.logger.info("Pulling config from Firebase")
        try:
            response = requests.post(
                "https://us-central1-usyd-attendance.cloudfunctions.net/getConfig",
                {
                    "secret": self.firebase_secret,
                    "bot_id": self.bot_id
                }
            )
            config = response.json()['config']
            self.server = config['server']
            self.course_name = config['course_name']
            self.course_id = config['course_id']
            self.access_token = config['token']
        except requests.exceptions.ConnectionError as err:
            self.logger.buzzer.setup_error()
            self.logger.error("Could not connect to server:", err)
            return True
        except KeyError as err:
            self.logger.buzzer.setup_error()
            self.logger.error("Could not obtain setup data:", err)
            return True
        except json.JSONDecodeError as err:
            self.logger.buzzer.setup_error()
            self.logger.error("Invalid response from Firebase:", err)
            return True
        self.ready = True
        return False
