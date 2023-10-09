import json
import pickle
from pymongo import MongoClient

client = MongoClient()
db = client.test_db
integrations = db.integrations


def process_state(state_id):
    state = integrations.find_one({"_id": state_id})

    for entity_name, entity in state["entities"].items():
        parse_fn = pickle.loads(entity["parseFn"])
        transform_fn = pickle.loads(entity["transformFn"])

        response = requests.get(entity["endpoint"])
        data = response.json()

        parsed_data = parse_fn(data)
        transformed_data = transform_fn(parsed_data)

        state["entities"][entity_name]["data"] = transformed_data

    integrations.update_one({"_id": state_id}, {"$set": state})

    return state
