from locust import HttpUser, TaskSet, task, between
import json

class PhoneRechargeTasks(TaskSet):

    @task
    def post_recharge(self):
        payload = {
            "charge_amount": 10,  
            "phone_number": 989035113419     
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token 68aec3f50236c1c8d174d9cd694a7c3c3f1f2e96'
        }
        
        with self.client.post("charge/phone-recharge/", data=json.dumps(payload), headers=headers, catch_response=True) as response:
            if response.status_code == 202:
                response.success()
            else:
                response.failure(f"Request failed with status code {response.status_code}")

class WebsiteUser(HttpUser):
    tasks = [PhoneRechargeTasks]
    wait_time = between(0, 0)
