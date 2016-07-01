__author__ = 'clyde'
from locust import HttpLocust, TaskSet, task
from io import StringIO

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        with open("state_test.csv")as self.fh:
            self.fc = self.fh.read()
            self.payload = StringIO(unicode(self.fc))

    def login(self):
        pass

    @task(2)
    def index(self):
        self.client.get("/")

    @task(1)
    def import_order(self):
        self.client.post("/orders/import", data=self.payload)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000