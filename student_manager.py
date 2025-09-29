import csv

class Student:
    def __init__(self, name, maths_marks, science_marks, english_marks, social_studies_marks, language_marks):
        self.student_name = name
        self.maths_marks = maths_marks
        self.science_marks = science_marks
        self.english_marks = english_marks
        self.social_studies_marks = social_studies_marks
        self.language_marks = language_marks

    def calculate_total(self):
        return (self.maths_marks + self.science_marks + self.english_marks +
                self.social_studies_marks + self.language_marks)

class StudentManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.students = self.load_students()

    def load_students(self):
        students = []
        try:
            with open(self.file_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        students.append(Student(
                            row['student_name'],
                            int(row['maths_marks']),
                            int(row['science_marks']),
                            int(row['english_marks']),
                            int(row['social_studies_marks']),
                            int(row['language_marks'])
                        ))
                    except ValueError:
                        print(f"Invalid data in row for student {row.get('student_name', 'unknown')}. Skipping.")
        except FileNotFoundError:
            print(f"File {self.file_path} not found. Starting with empty student list.")
        except Exception as e:
            print(f"Error loading file: {e}")
        return students

    def save_students(self):
        try:
            with open(self.file_path, mode='w', newline='') as file:
                fieldnames = ['student_name', 'maths_marks', 'science_marks', 'english_marks', 'social_studies_marks', 'language_marks']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for student in self.students:
                    writer.writerow({
                        'student_name': student.student_name,
                        'maths_marks': student.maths_marks,
                        'science_marks': student.science_marks,
                        'english_marks': student.english_marks,
                        'social_studies_marks': student.social_studies_marks,
                        'language_marks': student.language_marks
                    })
        except Exception as e:
            print(f"Error saving file: {e}")

    def add_student(self):
        try:
            name = input("Enter student name: ")
            maths = int(input("Enter maths marks: "))
            science = int(input("Enter science marks: "))
            english = int(input("Enter english marks: "))
            social = int(input("Enter social studies marks: "))
            language = int(input("Enter language marks: "))
            new_student = Student(name, maths, science, english, social, language)
            self.students.append(new_student)
            self.save_students()
            print("Student added successfully.")
        except ValueError:
            print("Invalid input. Marks must be integers.")
        except Exception as e:
            print(f"Error adding student: {e}")

    def update_student(self):
        try:
            name = input("Enter student name to update: ")
            found = False
            for student in self.students:
                if student.student_name == name:
                    found = True
                    subject = input("Enter subject to update (maths, science, english, social_studies, language): ").lower()
                    new_mark = int(input("Enter new mark: "))
                    if subject == 'maths':
                        student.maths_marks = new_mark
                    elif subject == 'science':
                        student.science_marks = new_mark
                    elif subject == 'english':
                        student.english_marks = new_mark
                    elif subject == 'social_studies':
                        student.social_studies_marks = new_mark
                    elif subject == 'language':
                        student.language_marks = new_mark
                    else:
                        print("Invalid subject.")
                        return
                    self.save_students()
                    print("Student updated successfully.")
                    return
            if not found:
                print("Student not found.")
        except ValueError:
            print("Invalid input. Marks must be integers.")
        except Exception as e:
            print(f"Error updating student: {e}")

    def delete_student(self):
        try:
            name = input("Enter student name to delete: ")
            for i, student in enumerate(self.students):
                if student.student_name == name:
                    del self.students[i]
                    self.save_students()
                    print("Student deleted successfully.")
                    return
            print("Student not found.")
        except Exception as e:
            print(f"Error deleting student: {e}")

    def show_analytics(self):
        if not self.students:
            print("No students available.")
            return
        try:
            total_sum = 0
            highest = float('-inf')
            lowest = float('inf')
            topper = None
            passed = 0
            failed = 0
            num_students = len(self.students)
            for student in self.students:
                total = student.calculate_total()
                total_sum += total
                if total > highest:
                    highest = total
                    topper = student.student_name
                if total < lowest:
                    lowest = total
                if total >= 200:
                    passed += 1
                else:
                    failed += 1
            mean = total_sum / num_students
            print(f"Topper: {topper}")
            print(f"Passed: {passed}")
            print(f"Failed: {failed}")
            print(f"Mean score: {mean:.2f}")
            print(f"Lowest score: {lowest}")
            print(f"Highest score: {highest}")
        except Exception as e:
            print(f"Error in analytics: {e}")

def main():
    file_path = 'students.csv'
    manager = StudentManager(file_path)
    while True:
        print("\nMenu:")
        print("1. Add student")
        print("2. Update student")
        print("3. Delete student")
        print("4. Show analytics")
        print("5. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            manager.add_student()
        elif choice == '2':
            manager.update_student()
        elif choice == '3':
            manager.delete_student()
        elif choice == '4':
            manager.show_analytics()
        elif choice == '5':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
