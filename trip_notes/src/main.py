import sys
import os

# Fix the import path so it works when run from the trip_notes/ root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Destination, TripCollection
from src.storage import load_trips, save_trips

def main():
    # On startup: load existing trips
    collection = load_trips()

    while True:
        print("\n=== Trip Notes ===")
        print("\n-- Data --")
        print("[1] Add destination")
        print("[2] List all destinations")
        print("[3] Mark as visited")
        print("[4] Show statistics")
        print("\n-- AI --")
        print("(coming soon)")
        print("\n[Q] Quit")
        
        choice = input("Select an option: ").strip()

        if choice == "1":
            name = input("Enter destination name: ")
            country = input("Enter country: ")
            try:
                budget = float(input("Enter estimated budget (USD): "))
                new_dest = Destination(name=name, country=country, budget=budget)
                collection.add(new_dest)
                save_trips(collection)
                print(f"Added {name} to your trips.")
            except ValueError:
                print("Invalid budget. Please enter a number.")

        elif choice == "2":
            if len(collection) == 0:
                print("No trips saved yet.")
            else:
                print("\n--- All Destinations ---")
                for i, trip in enumerate(collection.get_all(), 1):
                    visited_str = " (Visited)" if trip.visited else ""
                    print(f"{i}. {trip.name} ({trip.country}) - ${trip.budget:.2f}{visited_str}")
                    if trip.notes:
                        print(f"   Notes: {', '.join(trip.notes)}")
                    else:
                        print("   No notes added.")

        elif choice == "3":
            country_search = input("Enter country to search for: ")
            results = collection.search_by_country(country_search)
            if not results:
                print(f"No destinations found in {country_search}.")
            else:
                print(f"\n--- Search Results for '{country_search}' ---")
                for trip in results:
                    print(f"- {trip.name}: ${trip.budget:.2f}")

        elif choice == "4":
            if len(collection) == 0:
                print("No trips saved yet.")
            else:
                print("\n--- Select a destination to add a note ---")
                for i, trip in enumerate(collection.get_all(), 1):
                    print(f"{i}. {trip.name} ({trip.country})")
                
                try:
                    idx = int(input("Enter destination number: "))
                    if 1 <= idx <= len(collection):
                        trip = collection.get_by_index(idx - 1)
                        note = input(f"Enter note for {trip.name}: ")
                        trip.add_note(note)
                        save_trips(collection)
                        print("Note added.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == "5":
            if len(collection) == 0:
                print("No trips saved yet.")
            else:
                print("\n--- Mark a destination as Visited ---")
                for i, trip in enumerate(collection.get_all(), 1):
                    status = " [Visited]" if trip.visited else ""
                    print(f"{i}. {trip.name} ({trip.country}){status}")
                
                try:
                    idx = int(input("Enter destination number: "))
                    if 1 <= idx <= len(collection):
                        trip = collection.get_by_index(idx - 1)
                        collection.mark_visited(idx - 1)
                        save_trips(collection)
                        print(f"Marked {trip.name} as visited!")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == "6":
            wishlist = collection.get_wishlist()
            visited = collection.get_visited()
            
            print(f"\n--- Wishlist ({len(wishlist)}) ---")
            for trip in wishlist:
                print(f"- {trip.name} ({trip.country})")
            
            print(f"\n--- Visited ({len(visited)}) ---")
            for trip in visited:
                print(f"- {trip.name} ({trip.country})")

        elif choice.lower() == "q":
            print("Goodbye!")
            break

        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
