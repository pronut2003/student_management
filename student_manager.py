import csv

def load_students(file_path):
    students = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            students.append({
                'student_name': row['student_name'],
                'maths_marks': int(row['maths_marks']),
                'science_marks': int(row['science_marks']),
                'english_marks': int(row['english_marks']),
                'social_studies_marks': int(row['social_studies_marks']),
                'language_marks': int(row['language_marks'])
            })
    return students

def save_students(file_path, students):
    with open(file_path, mode='w', newline='') as file:
        fieldnames = ['student_name', 'maths_marks', 'science_marks', 'english_marks', 'social_studies_marks', 'language_marks']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for student in students:
            writer.writerow(student)

def calculate_total(student):
    return (student['maths_marks'] + student['science_marks'] + student['english_marks'] +
            student['social_studies_marks'] + student['language_marks'])

def add_student(students, file_path):
    name = input("Enter student name: ")
    maths = int(input("Enter maths marks: "))
    science = int(input("Enter science marks: "))
    english = int(input("Enter english marks: "))
    social = int(input("Enter social studies marks: "))
    language = int(input("Enter language marks: "))
    new_student = {
        'student_name': name,
        'maths_marks': maths,
        'science_marks': science,
        'english_marks': english,
        'social_studies_marks': social,
        'language_marks': language
    }
    students.append(new_student)
    save_students(file_path, students)
    print("Student added successfully.")

def update_student(students, file_path):
    name = input("Enter student name to update: ")
    for student in students:
        if student['student_name'] == name:
            subject = input("Enter subject to update (maths, science, english, social_studies, language): ")
            new_mark = int(input("Enter new mark: "))
            if subject == 'maths':
                student['maths_marks'] = new_mark
            elif subject == 'science':
                student['science_marks'] = new_mark
            elif subject == 'english':
                student['english_marks'] = new_mark
            elif subject == 'social_studies':
                student['social_studies_marks'] = new_mark
            elif subject == 'language':
                student['language_marks'] = new_mark
            else:
                print("Invalid subject.")
                return
            save_students(file_path, students)
            print("Student updated successfully.")
            return
    print("Student not found.")

def delete_student(students, file_path):
    name = input("Enter student name to delete: ")
    for i, student in enumerate(students):
        if student['student_name'] == name:
            del students[i]
            save_students(file_path, students)
            print("Student deleted successfully.")
            return
    print("Student not found.")

def show_analytics(students):
    if not students:
        print("No students available.")
        return
    totals = [calculate_total(s) for s in students]
    highest = max(totals)
    lowest = min(totals)
    mean = sum(totals) / len(totals)
    topper = next(s['student_name'] for s in students if calculate_total(s) == highest)
    passed = sum(1 for t in totals if t >= 200)
    failed = len(totals) - passed
    print(f"Topper: {topper}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Mean score: {mean:.2f}")
    print(f"Lowest score: {lowest}")
    print(f"Highest score: {highest}")

def main():
    file_path = 'students.csv'
    students = load_students(file_path)
    while True:
        print("\nMenu:")
        print("1. Add student")
        print("2. Update student")
        print("3. Delete student")
        print("4. Show analytics")
        print("5. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            add_student(students, file_path)
        elif choice == '2':
            update_student(students, file_path)
        elif choice == '3':
            delete_student(students, file_path)
        elif choice == '4':
            show_analytics(students)
        elif choice == '5':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()