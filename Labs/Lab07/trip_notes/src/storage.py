import os
import json
import dataclasses
from src.models import Destination, TripCollection

def load_trips() -> TripCollection:
    """Loads trip data from data/trips.json and returns a TripCollection."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "trips.json")
    
    collection = TripCollection()
    
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            for d in data:
                collection.add(Destination(**d))
                
    return collection

def save_trips(collection: TripCollection) -> None:
    """Saves the TripCollection to data/trips.json."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "trips.json")
    
    # Create the data/ directory if it does not exist
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    
    # Convert each Destination to dict using dataclasses.asdict()
    list_of_dicts = [dataclasses.asdict(d) for d in collection.get_all()]
    
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(list_of_dicts, f, indent=2)
