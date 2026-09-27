import json
import os
import sys

DATA_FILE = "students.json"

# ==========================================
# File I/O & Data Persistence Layer
# ==========================================

def load_students():
    """Load students from the JSON file. Initialize if file does not exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print("\n[!] Warning: Data file corrupted or unreadable. Starting with empty dataset.")
        return []

def save_students(students):
    """Save the list of student dictionaries back into the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
    except IOError as e:
        print(f"\n[!] Failed to save data: {e}")

# ==========================================
# CRUD Operations
# ==========================================

def create_student():
    """C: Add a new student record."""
    print("\n--- Add New Student ---")
    students = load_students()

    while True:
        student_id = input("Enter Student ID: ").strip()
        if not student_id:
            print("ID cannot be empty.")
            continue
        if any(s["id"] == student_id for s in students):
            print(f"Error: A student with ID '{student_id}' already exists.")
            return
        break

    name = input("Enter Full Name: ").strip()
    course = input("Enter Course/Major: ").strip()

    # Numeric validation: Age
    while True:
        try:
            age = int(input("Enter Age: ").strip())
            if age <= 0:
                print("Age must be a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for age.")

    # Numeric validation: GPA
    while True:
        try:
            gpa = float(input("Enter GPA (0.0 - 4.0): ").strip())
            if not (0.0 <= gpa <= 4.0):
                print("GPA must be between 0.0 and 4.0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid decimal number for GPA.")

    new_student = {
        "id": student_id,
        "name": name,
        "age": age,
        "course": course,
        "gpa": round(gpa, 2)
    }

    students.append(new_student)
    save_students(students)
    print(f"\n[+] Success: Student '{name}' (ID: {student_id}) added.")

def read_all_students():
    """R: Display all student records."""
    print("\n--- Registered Students ---")
    students = load_students()

    if not students:
        print("No student records found.")
        return

    # Print formatted table header
    print(f"{'ID':<10} | {'Name':<22} | {'Age':<5} | {'Course':<20} | {'GPA':<5}")
    print("-" * 72)
    for s in students:
        print(f"{s['id']:<10} | {s['name']:<22} | {s['age']:<5} | {s['course']:<20} | {s['gpa']:<5.2f}")

def search_student():
    """R: Search and view a single student by ID."""
    print("\n--- Search Student ---")
    student_id = input("Enter Student ID to search: ").strip()
    students = load_students()

    for s in students:
        if s["id"] == student_id:
            print("\nStudent Record Found:")
            print(f"  ID:     {s['id']}")
            print(f"  Name:   {s['name']}")
            print(f"  Age:    {s['age']}")
            print(f"  Course: {s['course']}")
            print(f"  GPA:    {s['gpa']:.2f}")
            return

    print(f"\n[!] No student found with ID: {student_id}")

def update_student():
    """U: Update an existing student record."""
    print("\n--- Update Student Record ---")
    student_id = input("Enter Student ID to update: ").strip()
    students = load_students()

    for s in students:
        if s["id"] == student_id:
            print(f"\nUpdating record for: {s['name']} (Press Enter to keep existing value)")

            new_name = input(f"New Name [{s['name']}]: ").strip()
            if new_name:
                s["name"] = new_name

            new_age = input(f"New Age [{s['age']}]: ").strip()
            if new_age:
                try:
                    s["age"] = int(new_age)
                except ValueError:
                    print("Invalid input for age. Retaining previous value.")

            new_course = input(f"New Course [{s['course']}]: ").strip()
            if new_course:
                s["course"] = new_course

            new_gpa = input(f"New GPA [{s['gpa']}]: ").strip()
            if new_gpa:
                try:
                    val = float(new_gpa)
                    if 0.0 <= val <= 4.0:
                        s["gpa"] = round(val, 2)
                    else:
                        print("GPA out of range (0.0 - 4.0). Retaining previous value.")
                except ValueError:
                    print("Invalid input for GPA. Retaining previous value.")

            save_students(students)
            print(f"\n[+] Success: Student record for ID '{student_id}' has been updated.")
            return

    print(f"\n[!] Student with ID '{student_id}' not found.")

def delete_student():
    """D: Delete a student record by ID."""
    print("\n--- Delete Student Record ---")
    student_id = input("Enter Student ID to delete: ").strip()
    students = load_students()

    updated_records = [s for s in students if s["id"] != student_id]

    if len(updated_records) == len(students):
        print(f"\n[!] Student with ID '{student_id}' not found.")
    else:
        save_students(updated_records)
        print(f"\n[+] Success: Student record with ID '{student_id}' was removed.")

# ==========================================
# Main Menu & Controller
# ==========================================

def display_menu():
    print("\n" + "=" * 36)
    print("  STUDENT RECORD MANAGEMENT SYSTEM  ")
    print("=" * 36)
    print("1. Add New Student")
    print("2. View All Students")
    print("3. Search Student by ID")
    print("4. Update Student Details")
    print("5. Delete Student Record")
    print("6. Exit")
    print("=" * 36)

def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            create_student()
        elif choice == "2":
            read_all_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("\nExiting program. Goodbye!\n")
            sys.exit(0)
        else:
            print("\n[!] Invalid selection. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()