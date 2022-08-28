import requests as requests
import os

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 ' \
             'Safari/537.36'
headers = {'User-Agent': USER_AGENT}

APPOINTMENT_URL = "https://icp.administracionelectronica.gob.es/icpplustieb/citar?p=8&locale=es"
NO_APPOINTMENT_STRING = "En este momento no hay citas disponibles en esta sede"

SLACK_URL = os.environ["SLACK_WEBHOOK_URL"]
SLACK_MEMBER_ID = os.environ["SLACK_MEMBER_ID"]


def lambda_handler(event, _):
    resp = requests.get(APPOINTMENT_URL, headers=headers, verify=False)
    if resp.status_code == 200:
        if NO_APPOINTMENT_STRING not in resp.text:
            print("Found an appointment")
            requests.post(SLACK_URL, json={"text": f"<@{SLACK_MEMBER_ID}> <{APPOINTMENT_URL}|Appointment available>"})
            return
        requests.post(SLACK_URL, json={"text": f"<@{SLACK_MEMBER_ID}> <{APPOINTMENT_URL}|No Appointment available!!>"})
        print("Did not find an appointment")
        return {"statusCode": 200}

    if resp.status_code == 429:
        print("Too many requests")
        requests.post(SLACK_URL, json={"text": f"<@{SLACK_MEMBER_ID}> Too many requests"})
        return {"statusCode": 200}
    # Some other error lets log that too!
    print(f"Received {resp.status_code}\n{resp.text}\nPlease investigate")
    requests.post(SLACK_URL, json={"text": f"<@{SLACK_MEMBER_ID}> Received {resp.status_code}\n{resp.text}\nPlease "
                                           f"investigate"})
    return {"statusCode": 200}


if __name__ == "__main__":
    lambda_handler({}, {})
