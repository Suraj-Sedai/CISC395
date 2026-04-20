import sys
import os

# Fix the import path so it works when run from the trip_notes/ root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Destination, TripCollection
from src.ai_assistant import ask, TRAVEL_SYSTEM_PROMPT, generate_trip_briefing, rag_ask
from src.rag import build_index
from src.storage import load_trips, save_trips
from src.tools import run_agent

def main():
    # On startup: load existing trips
    collection = load_trips()

    while True:
        print("\n=== Trip Notes ===")
        print("\n-- Data --")
        print("[1] Add destination       [2] List all destinations")
        print("[3] Mark as visited       [4] Show statistics")
        print("\n-- AI --")
        print("[6] Ask AI                [7] Trip Briefing")
        print("[8] Search my guides      [10] AI Travel Agent")
        print("\n[R] Rebuild search index")
        print("[Q] Quit")
        
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
            question = input("Your question: ")
            result = ask(question, system_prompt=TRAVEL_SYSTEM_PROMPT)

            if result is None:
                print("Could not get a response from the AI assistant.")
                continue

            print(result)

            save_note = input("Save this as a note on a trip? (y/n): ").strip().lower()
            if save_note == "y":
                destinations = collection.get_all()
                if not destinations:
                    print("No trips saved yet.")
                else:
                    for i, trip in enumerate(destinations, 1):
                        print(f"{i}. {trip.name} ({trip.country})")

                    try:
                        index = int(input("Trip number: ")) - 1
                        if not 0 <= index < len(destinations):
                            raise IndexError
                        trip = collection.get_by_index(index)
                        trip.add_note(result)
                        save_trips(collection)
                        print(f"Saved as a note on {trip.name}.")
                    except (ValueError, IndexError):
                        print("Invalid trip number.")

        elif choice == "7":
            destinations = collection.get_all()
            if not destinations:
                print("No trips saved yet.")
                continue

            for i, dest in enumerate(destinations, 1):
                print(f"  [{i}] {dest.name}, {dest.country}")

            try:
                index = int(input("Select trip number: ")) - 1
            except ValueError:
                print("Invalid selection.")
                continue

            if not 0 <= index < len(destinations):
                print("Invalid selection.")
                continue

            dest = destinations[index]
            print(f"Generating briefing for {dest.name}...")
            result = generate_trip_briefing(dest.name, dest.country, dest.notes)

            if result is None:
                print("Briefing failed. Check your API connection.")
                continue

            print(f"\n--- {dest.name} Briefing ---")
            print(f"Overview:\n{result['overview']}")
            print(f"\nPacking List:\n{result['packing_list']}")

        elif choice == "8":
            question = input("Your question: ")
            answer = rag_ask(question)
            print(answer)

        elif choice == "10":
            print("The agent can calculate budgets, check real-time weather, and search your travel guides.")
            question = input("Your question: ")
            print("\nThinking...\n")
            result = run_agent(question)

            if result is None:
                print("Could not get a response from the AI Travel Agent.")
                continue

            print("\nAgent answer:\n" + result)

            save_note = input("Save this as a note on a trip? (y/n): ").strip().lower()
            if save_note == "y":
                destinations = collection.get_all()
                if not destinations:
                    print("No trips saved yet.")
                else:
                    for i, trip in enumerate(destinations, 1):
                        print(f"{i}. {trip.name} ({trip.country})")

                    try:
                        index = int(input("Trip number: ")) - 1
                        if not 0 <= index < len(destinations):
                            raise IndexError
                        trip = collection.get_by_index(index)
                        trip.add_note(result)
                        save_trips(collection)
                        print(f"Saved as a note on {trip.name}.")
                    except (ValueError, IndexError):
                        print("Invalid trip number.")

        elif choice.lower() == "r":
            print("Rebuilding index from guides/...")
            build_index(force=True)
            print("Done. Use [8] to search your updated guides.")

        elif choice.lower() == "q":
            print("Goodbye!")
            break

        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
