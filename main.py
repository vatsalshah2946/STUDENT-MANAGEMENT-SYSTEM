import tkinter as tk
from tkinter import messagebox, simpledialog

# ── Placeholder functions (replace with your real logic) ──────────
def register_student():
    name = simpledialog.askstring("Register", "Student Name:")
    sid  = simpledialog.askstring("Register", "Student ID:")
    if name and sid:
        messagebox.showinfo("Success", f"Registered: {name} ({sid})")

def student_login():
    sid = simpledialog.askstring("Login", "Enter Student ID:")
    if sid:
        return {"id": sid, "name": "Student"}
    return None

def student_menu(student):
    messagebox.showinfo("Student Menu", f"Welcome, {student['name']}!")

def admin_menu():
    messagebox.showinfo("Admin", "Admin panel opened.")
# ──────────────────────────────────────────────────────────────────

# ── GUI Setup ─────────────────────────────────────────────────────
root = tk.Tk()
root.title("Student Management System")
root.geometry("340x320")
root.configure(bg="#f5f5f5")
root.resizable(False, False)

# Title
tk.Label(
    root, text="Student Management",
    font=("Segoe UI", 15, "bold"),
    bg="#f5f5f5", fg="#333"
).pack(pady=(30, 20))

# Shared button config
BTN = dict(
    font=("Segoe UI", 11), width=22, pady=6,
    bg="#4a90d9", fg="white",
    activebackground="#357ab8", activeforeground="white",
    relief="flat", cursor="hand2", bd=0
)

# ── Button callbacks ──────────────────────────────────────────────
def on_register():
    register_student()

def on_login():
    student = student_login()
    if student:
        student_menu(student)

def on_admin():
    admin_menu()

def on_exit():
    if messagebox.askyesno("Exit", "Quit the application?"):
        root.destroy()

# ── Buttons ───────────────────────────────────────────────────────
tk.Button(root, text="Register Student",  command=on_register, **BTN).pack(pady=4)
tk.Button(root, text="Student Login",     command=on_login,    **BTN).pack(pady=4)
tk.Button(root, text="Admin Menu",        command=on_admin,    **BTN).pack(pady=4)
tk.Button(root, text="Exit",              command=on_exit,
          **{**BTN, "bg": "#e74c3c", "activebackground": "#c0392b"}).pack(pady=4)

root.mainloop()
import tkinter as tk
import json
import os
from datetime import datetime
STUDENT_FILE = "students.json"
QUESTION_FILE = "questions.json"
RESULT_FILE = "results.json"
# ---------------- FILE HANDLING ----------------
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                return json.load(file)
            except:
                return []
    return []
def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# ---------------- STUDENT REGISTRATION ----------------

def register_student():
    students = load_data(STUDENT_FILE)

    print("\n===== STUDENT REGISTRATION =====")

    name = input("Enter student name: ")
    roll_no = input("Enter roll number: ")
    password = input("Create password: ")

    for student in students:
        if student["roll_no"] == roll_no:
            print("Roll number already registered!")
            return

    student = {
        "name": name,
        "roll_no": roll_no,
        "password": password
    }

    students.append(student)
    save_data(STUDENT_FILE, students)

    print("Registration successful!")


# ---------------- STUDENT LOGIN ----------------

def student_login():
    students = load_data(STUDENT_FILE)

    print("\n===== STUDENT LOGIN =====")

    roll_no = input("Enter roll number: ")
    password = input("Enter password: ")

    for student in students:
        if student["roll_no"] == roll_no and student["password"] == password:
            print("\nLogin successful!")
            print("Welcome,", student["name"])
            return student

    print("Invalid roll number or password!")
    return None


# ---------------- EXAM ----------------

def start_exam(student):
    questions = load_data(QUESTION_FILE)

    if not questions:
        print("No questions available.")
        return

    print("\n================================")
    print("        ONLINE EXAMINATION")
    print("================================")
    print("Student:", student["name"])
    print("Roll No:", student["roll_no"])
    print("Total Questions:", len(questions))
    print("Each question carries 1 mark.")
    print("================================")

    input("\nPress Enter to start the examination...")

    score = 0

    for i, question in enumerate(questions, start=1):

        print("\nQuestion", i)
        print(question["question"])

        for option in question["options"]:
            print(option)

        answer = input("Enter your answer (A/B/C/D): ").upper()

        if answer == question["answer"]:
            print("Correct!")
            score += 1
        else:
            print("Wrong!")
            print("Correct answer:", question["answer"])

    total = len(questions)
    percentage = (score / total) * 100

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    elif percentage >= 40:
        grade = "E"
    else:
        grade = "F"

    status = "PASS" if percentage >= 40 else "FAIL"

    print("\n================================")
    print("          EXAM RESULT")
    print("================================")
    print("Student Name :", student["name"])
    print("Roll Number  :", student["roll_no"])
    print("Marks        :", score, "/", total)
    print("Percentage   :", round(percentage, 2), "%")
    print("Grade        :", grade)
    print("Status       :", status)
    print("================================")

    result = {
        "name": student["name"],
        "roll_no": student["roll_no"],
        "marks": score,
        "total": total,
        "percentage": round(percentage, 2),
        "grade": grade,
        "status": status,
        "date": datetime.now().strftime("%d-%m-%Y %H:%M")
    }

    results = load_data(RESULT_FILE)
    results.append(result)
    save_data(RESULT_FILE, results)


# ---------------- VIEW RESULT HISTORY ----------------

def view_results(student):
    results = load_data(RESULT_FILE)

    student_results = []

    for result in results:
        if result["roll_no"] == student["roll_no"]:
            student_results.append(result)

    print("\n===== RESULT HISTORY =====")

    if not student_results:
        print("No examination results found.")
        return

    for i, result in enumerate(student_results, start=1):
        print("\nAttempt", i)
        print("Date       :", result["date"])
        print("Marks      :", result["marks"], "/", result["total"])
        print("Percentage :", result["percentage"], "%")
        print("Grade      :", result["grade"])
        print("Status     :", result["status"])


# ---------------- ADMIN: ADD QUESTION ----------------

def add_question():
    questions = load_data(QUESTION_FILE)

    print("\n===== ADD QUESTION =====")

    question = input("Enter question: ")

    options = []

    options.append("A. " + input("Enter option A: "))
    options.append("B. " + input("Enter option B: "))
    options.append("C. " + input("Enter option C: "))
    options.append("D. " + input("Enter option D: "))

    answer = input("Enter correct answer (A/B/C/D): ").upper()

    if answer not in ["A", "B", "C", "D"]:
        print("Invalid answer!")
        return

    new_question = {
        "question": question,
        "options": options,
        "answer": answer
    }

    questions.append(new_question)
    save_data(QUESTION_FILE, questions)

    print("Question added successfully!")

# ---------------- ADMIN: VIEW RESULTS ----------------
def view_all_results():
    results = load_data(RESULT_FILE)

    print("\n========== ALL RESULTS ==========")

    if not results:
        print("No results available.")
        return

    for result in results:
        print("\nStudent:", result["name"])
        print("Roll No:", result["roll_no"])
        print("Marks:", result["marks"], "/", result["total"])
        print("Percentage:", result["percentage"], "%")
        print("Grade:", result["grade"])
        print("Status:", result["status"])
        print("Date:", result["date"])


# ---------------- ADMIN LOGIN ----------------

def admin_menu():
    print("\n===== ADMIN LOGIN =====")

    username = input("Username: ")
    password = input("Password: ")

    if username != "admin" or password != "1234":
        print("Invalid admin credentials!")
        return

    while True:
        print("\n========== ADMIN MENU ==========")
        print("1. Add Question")
        print("2. View All Results")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_question()

        elif choice == "2":
            view_all_results()

        elif choice == "3":
            break

        else:
            print("Invalid choice!")


# ---------------- STUDENT MENU ----------------

def student_menu(student):
    while True:
        print("\n========== STUDENT MENU ==========")
        print("1. Start Examination")
        print("2. View Result History")
        print("3. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            start_exam(student)

        elif choice == "2":
            view_results(student)

        elif choice == "3":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice!")


# ---------------- MAIN PROGRAM ----------------

def main():
    while True:
        print("\n====================================")
        print("      ONLINE EXAMINATION SYSTEM")
        print("====================================")
        print("1. Student Registration")
        print("2. Student Login")
        print("3. Admin Login")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_student()

        elif choice == "2":
            student = student_login()

            if student:
                student_menu(student)

        elif choice == "3":
            admin_menu()

        elif choice == "4":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice!")
main()