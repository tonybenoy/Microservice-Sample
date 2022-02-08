import os
import redis
import json

from twilio.rest import Client
from multiprocessing import Process

db = redis.Redis(host="0.0.0.0")


def sub():
    pubsub = db.pubsub()
    pubsub.subscribe("sms")
    for message in pubsub.listen():
        if message.get("type") == "message":
            data = json.loads(message.get("data"))
            print("%s : %s" % (name, data))

            account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
            auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

            body = data.get("message")
            from_ = data.get("from")
            to = data.get("to")

            client = Client(account_sid, auth_token)
            message = client.messages.create(from_=from_, to=to, body=body)
            print("message id: %s" % message.sid)



if __name__ == "__main__":
    Process(target=sub).start()
