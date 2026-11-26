
import json

from locust import HttpUser, task, constant

CONFIG = json.loads('{"method": "POST", "url_endpoint": "http://sdfsdf.md", "headers": {}, "params_url": {}, "body": {}, "nb_threads": 30, "duree_secondes": 600, "ramp_up": 60, "think_time": 0, "nb_repetitions": 1}')


class PerformanceUser(HttpUser):

    wait_time = constant(CONFIG["think_time"])

    @task
    def execute_request(self):

        method = CONFIG["method"].upper()

        url = CONFIG["url_endpoint"]

        headers = CONFIG.get("headers") or {}

        params = CONFIG.get("params_url") or {}

        body = CONFIG.get("body") or {}

        if method == "GET":

            self.client.get(
                url,
                headers=headers,
                params=params
            )

        elif method == "POST":

            self.client.post(
                url,
                json=body,
                headers=headers,
                params=params
            )

        elif method == "PUT":

            self.client.put(
                url,
                json=body,
                headers=headers,
                params=params
            )

        elif method == "PATCH":

            self.client.patch(
                url,
                json=body,
                headers=headers,
                params=params
            )

        elif method == "DELETE":

            self.client.delete(
                url,
                headers=headers,
                params=params
            )
