# task_manager.py
# TechStart — Student Task Manager (Prototype)
# Run: python task_manager.py

tasks = []

def add_task(name, priority="Medium"):
    task = {
        "id": len(tasks) + 1,
        "name": name,
        "priority": priority,
        "status": "Pending"
    }
    tasks.append(task)
    print(f"Added: [{task['id']}] {name} ({priority})")

def view_tasks():
    if not tasks:
        print("No tasks yet.")
        return
    print("\n--- Task List ---")
    for t in tasks:
        print(f"[{t['id']}] {t['name']} | {t['priority']} | {t['status']}")
    print()

def complete_task(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "Done"
            print(f"Marked as done: {t['name']}")
            return
    print("Task not found.")

def task_summary():
    status_counts = {
        "Done": 0,
        "In Progress": 0,
        "Blocked": 0,
        "To Do": 0
    }

    for t in tasks:
        status = t["status"]
        if status == "Done":
            status_counts["Done"] += 1
        elif status == "In Progress":
            status_counts["In Progress"] += 1
        elif status == "Blocked":
            status_counts["Blocked"] += 1
        else:
            status_counts["To Do"] += 1

    total_tasks = len(tasks)

    print("\n=== Task Summary ===")
    print(f"Done          : {status_counts['Done']}")
    print(f"In Progress   : {status_counts['In Progress']}")
    print(f"Blocked       : {status_counts['Blocked']}")
    print(f"To Do         : {status_counts['To Do']}")
    print(f"Total tasks   : {total_tasks}")

    if status_counts["Blocked"] > 0:
        print("\nWARNING: Some tasks are Blocked!")

def main():
    add_task("Design login page", "High")
    add_task("Write unit tests", "Medium")
    add_task("Update documentation", "Low")

    view_tasks()
    complete_task(1)
    view_tasks()

if __name__ == "__main__":
    main()