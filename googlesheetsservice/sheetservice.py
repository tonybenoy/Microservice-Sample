import redis

from multiprocessing import Process
import json
from pprint import pprint

from googleapiclient import discovery

db = redis.Redis(host="0.0.0.0")


def sub():
    pubsub = db.pubsub()
    pubsub.subscribe("google-sheet")
    for message in pubsub.listen():
        if message.get("type") == "add-to-sheet":
            data = json.loads(message.get("data"))
            append_to_sheet(data)


if __name__ == "__main__":
    Process(target=sub).start()


def append_to_sheet(data: dict):
    credentials = None
    service = discovery.build("sheets", "v4", credentials=credentials)
    spreadsheet_id = "my-spreadsheet-id"
    range_ = "my-range"
    value_input_option = ""
    insert_data_option = ""
    value_range_body = {}

    request = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=range_,
            valueInputOption=value_input_option,
            insertDataOption=insert_data_option,
            body=value_range_body,
        )
    )
    response = request.execute()
    pprint(response)
