import json
from datetime import datetime
import os

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.filename = "tasks.json"
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from JSON file if it exists."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.tasks = json.load(file)

    def save_tasks(self):
        """Save tasks to JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=2)

    def add_task(self, title, description, due_date=None):
        """Add a new task."""
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'due_date': due_date,
            'status': 'Pending',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    def list_tasks(self, show_completed=True):
        """List all tasks."""
        tasks_to_show = self.tasks if show_completed else [t for t in self.tasks if t['status'] != 'Completed']
        return tasks_to_show

    def complete_task(self, task_id):
        """Mark a task as completed."""
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = 'Completed'
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id):
        """Delete a task."""
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.save_tasks()

def print_task(task):
    """Print a single task in a formatted way with colors."""
    colors = {
        "Pending": "\033[93m",  # Yellow
        "Completed": "\033[92m",  # Green
        "reset": "\033[0m"
    }
    
    status_color = colors.get(task['status'], colors["reset"])
    
    print(f"\nTask #{task['id']}")
    print(f"Title: {task['title']}")
    print(f"Description: {task['description']}")
    print(f"Status: {status_color}{task['status']}{colors['reset']}")
    print(f"Created: {task['created_at']}")
    
    if task['due_date']:
        print(f"Due: {task['due_date']}")
    
    print("-" * 30)

def main():
    manager = TaskManager()
    
    while True:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ")
            due_date = due_date if due_date else None
            task = manager.add_task(title, description, due_date)
            print("\nTask added successfully!")
            print_task(task)
            
        elif choice == '2':
            tasks = manager.list_tasks()
            if not tasks:
                print("\nNo tasks found!")
            for task in tasks:
                print_task(task)
                
        elif choice == '3':
            task_id = int(input("Enter task ID to mark as completed: "))
            if manager.complete_task(task_id):
                print(f"\nTask #{task_id} marked as completed!")
            else:
                print(f"\nTask #{task_id} not found!")
                
        elif choice == '4':
            task_id = int(input("Enter task ID to delete: "))
            manager.delete_task(task_id)
            print(f"\nTask #{task_id} deleted!")
            
        elif choice == '5':
            print("\nGoodbye!")
            break
            
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()