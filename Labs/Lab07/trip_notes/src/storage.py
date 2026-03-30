import os
import json
from dataclasses import asdict
from src.models import Destination, TripCollection

def load_trips() -> TripCollection:
    """Loads trip data from data/trips.json and returns a TripCollection."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "trips.json")
    
    collection = TripCollection()
    
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    # Convert dict back to Destination object
                    # asdict() will have name, country, budget, notes, date_added
                    destination = Destination(**item)
                    collection.add(destination)
        except (json.JSONDecodeError, TypeError, KeyError):
            # In case of corrupted file, return empty collection
            pass
            
    return collection

def save_trips(collection: TripCollection) -> None:
    """Saves the TripCollection to data/trips.json."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "trips.json")
    
    # Create the data/ directory if it does not exist
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    
    # Convert each Destination to dict
    list_of_dicts = [asdict(d) for d in collection.get_all()]
    
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(list_of_dicts, f, indent=2)
