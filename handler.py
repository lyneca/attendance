import requests
import time
from datetime import datetime

class Handler:
    def __init__(self, logger, config):
        self.config = config
        self.logger = logger
        self.assignments = None

    def get_headers(self):
        return {
            "Authorization": "Bearer " + self.config.access_token,
            "Content-Type": "multipart/form-data"
        }


    def get(self, url):
        """Send a GET request to the Canvas server"""
        return requests.get(self.config.server + url, headers=self.get_headers())

    def get_assignments(self):
        """Attempt to request the list of attendance assignments"""
        while True:
            try:
                self.logger.info("Getting list of assignments")
                self.assignments = self.get("/courses/{}/assignments?per_page=50".format(
                    self.config.course)).json()
                break
            except requests.exceptions.ConnectionError:
                self.logger.error("Could not connect to Canvas")
                time.sleep(3)
                continue
        self.logger.info("Successfully requested assignment list")

    def get_aid(self):
        """Get the assignment corresponding to this date"""
        if not self.assignments:
            return None
        date = datetime.now().isoformat().split("T")[0]
        aids = [
            x for x in self.assignments if "attendance" in x["name"].lower()
            and "due_at" in x
            and x["due_at"] is not None
            and date == x["due_at"].split("T")[0]
        ]
        if aids:
            self.logger.info("Got AID:", aids[0]["id"])
            return aids[0]["id"]
        return None

    def send(self, sid):
        """Attempt to send scanned card data to Canvas"""
        aid = self.get_aid()
        self.logger.info("Sending", sid)

        if aid:
            url = self.config.server + \
                "/courses/{}/assignments/{}/submissions/sis_user_id:{}".format(
                    self.config.course, aid, sid
                )
            response = requests.put(
                url, "submission[posted_grade]=1", headers=self.get_headers())
            if response.ok:
                self.logger.info("Sent")
            else:
                self.logger.error(response.status_code, response.reason)
                print(response.content)
        else:
            self.logger.error("No assignment found.")
