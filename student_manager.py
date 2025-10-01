import csv
import os

class Student:
    def __init__(self, name, maths_marks, science_marks, english_marks, social_studies_marks, language_marks):
        if not isinstance(name, str):
            raise TypeError("Student name must be a string")
        if not all(isinstance(mark, int) for mark in [maths_marks, science_marks, english_marks, social_studies_marks, language_marks]):
            raise TypeError("Marks must be integers")
        if not all(0 <= mark <= 100 for mark in [maths_marks, science_marks, english_marks, social_studies_marks, language_marks]):
            raise ValueError("Marks must be between 0 and 100")
        self.student_name = name
        self.maths_marks = maths_marks
        self.science_marks = science_marks
        self.english_marks = english_marks
        self.social_studies_marks = social_studies_marks
        self.language_marks = language_marks

    def calculate_total(self):
        """Calculate the total marks for the student."""
        return (self.maths_marks + self.science_marks + self.english_marks +
                self.social_studies_marks + self.language_marks)

class StudentManager:
    def __init__(self, file_path):
        if not isinstance(file_path, str):
            raise TypeError("File path must be a string")
        self.file_path = file_path
        self.students = self.load_students()

    def load_students(self):
        """Load students from CSV file. Return list of students or empty list on failure."""
        students = []
        required_headers = ['student_name', 'maths_marks', 'science_marks', 'english_marks',
                            'social_studies_marks', 'language_marks']
        
        try:
            if not os.path.exists(self.file_path):
                print(f"File {self.file_path} not found. Starting with empty student list.")
                return students
            
            with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                if not all(header in reader.fieldnames for header in required_headers):
                    print(f"Error: CSV file missing required headers: {required_headers}")
                    return students
                
                for row in reader:
                    if not row['student_name'].strip():
                        print("Warning: Skipping empty row in CSV.")
                        continue
                    try:
                        marks = [
                            int(row['maths_marks']),
                            int(row['science_marks']),
                            int(row['english_marks']),
                            int(row['social_studies_marks']),
                            int(row['language_marks'])
                        ]
                        if any(mark < 0 for mark in marks):
                            print(f"Negative marks for student {row['student_name']}. Skipping.")
                            continue
                        students.append(Student(row['student_name'], *marks))
                    except (ValueError, KeyError) as e:
                        print(f"Invalid data for student {row.get('student_name', 'unknown')}: {e}. Skipping.")
        except PermissionError:
            print(f"Error: Permission denied accessing {self.file_path}.")
        except Exception as e:
            print(f"Error loading file: {e}")
        return students

    def save_students(self):
        """Save students to CSV file. Return True on success, False on failure."""
        try:
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ['student_name', 'maths_marks', 'science_marks', 'english_marks',
                              'social_studies_marks', 'language_marks']
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
            return True
        except PermissionError:
            print(f"Error: Permission denied writing to {self.file_path}.")
            return False
        except Exception as e:
            print(f"Error saving file: {e}")
            return False

    def add_student(self):
        """Add a new student. Return True on success, False on failure."""
        try:
            name = input("Enter student name: ").strip()
            if not name:
                print("Error: Student name cannot be empty.")
                return False
            marks = []
            subjects = ['maths', 'science', 'english', 'social studies', 'language']
            for subject in subjects:
                while True:
                    mark = input(f"Enter {subject} marks (0-100): ").strip()
                    try:
                        mark = int(mark)
                        if not 0 <= mark <= 100:
                            print(f"Error: {subject} marks must be between 0 and 100.")
                            continue
                        marks.append(mark)
                        break
                    except ValueError:
                        print(f"Error: {subject} marks must be a valid integer.")
            new_student = Student(name, *marks)
            self.students.append(new_student)
            if self.save_students():
                print("Student added successfully.")
                return True
            else:
                print("Failed to save student data.")
                return False
        except KeyboardInterrupt:
            print("\nInput interrupted. Student not added.")
            return False
        except Exception as e:
            print(f"Error adding student: {e}")
            return False

    def update_student(self):
        """Update a student's marks. Return True on success, False on failure."""
        try:
            name = input("Enter student name to update: ").strip()
            if not name:
                print("Error: Student name cannot be empty.")
                return False
            found = False
            for student in self.students:
                if student.student_name == name:
                    found = True
                    subject = input("Enter subject to update (maths, science, english, social_studies, language): ").lower().strip()
                    if subject not in ['maths', 'science', 'english', 'social_studies', 'language']:
                        print("Error: Invalid subject.")
                        return False
                    while True:
                        try:
                            new_mark = input("Enter new mark (0-100): ").strip()
                            new_mark = int(new_mark)
                            if not 0 <= new_mark <= 100:
                                print("Error: Marks must be between 0 and 100.")
                                continue
                            break
                        except ValueError:
                            print("Error: Marks must be a valid integer.")
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
                    if self.save_students():
                        print("Student updated successfully.")
                        return True
                    else:
                        print("Failed to save updated data.")
                        return False
            if not found:
                print("Student not found.")
                return False
        except KeyboardInterrupt:
            print("\nInput interrupted. Student not updated.")
            return False
        except Exception as e:
            print(f"Error updating student: {e}")
            return False

    def delete_student(self):
        """Delete a student. Return True on success, False on failure."""
        try:
            name = input("Enter student name to delete: ").strip()
            if not name:
                print("Error: Student name cannot be empty.")
                return False
            for i, student in enumerate(self.students):
                if student.student_name == name:
                    del self.students[i]
                    if self.save_students():
                        print("Student deleted successfully.")
                        return True
                    else:
                        print("Failed to save updated data.")
                        return False
            print("Student not found.")
            return False
        except KeyboardInterrupt:
            print("\nInput interrupted. Student not deleted.")
            return False
        except Exception as e:
            print(f"Error deleting student: {e}")
            return False

    def show_analytics(self):
        """Show simple analytics. Return results as a dictionary or None if no valid data."""
        if not self.students:
            print("No students found.")
            return None

        try:
            total_marks = 0
            highest_marks = 0
            lowest_marks = 0
            topper_name = ""
            passed_count = 0
            failed_count = 0
            valid_student_count = 0
            first_valid_student = True

            for student in self.students:
                marks = [
                    student.maths_marks,
                    student.science_marks,
                    student.english_marks,
                    student.social_studies_marks,
                    student.language_marks
                ]
                if not all(isinstance(mark, (int)) for mark in marks):
                    print(f"Skipping {student.student_name}: Invalid or missing marks.")
                    continue
                if any(mark < 0 for mark in marks):
                    print(f"Skipping {student.student_name}: Negative marks found.")
                    continue

                total = student.calculate_total()
                valid_student_count += 1
                total_marks += total

                if first_valid_student or total >= highest_marks:
                    highest_marks = total
                    topper_name = student.student_name
                    if first_valid_student:
                        first_valid_student = False

                if first_valid_student or total <= lowest_marks:
                    lowest_marks = total
                    if first_valid_student:
                        first_valid_student = False

                if total >= 200:
                    passed_count += 1
                else:
                    failed_count += 1

            if valid_student_count == 0:
                print("No valid student data to analyze.")
                return None

            mean_marks = total_marks / valid_student_count
            results = {
                "topper": topper_name,
                "passed": passed_count,
                "failed": failed_count,
                "mean": round(mean_marks, 2),
                "lowest": lowest_marks,
                "highest": highest_marks
            }

            print(f"Topper: {topper_name}")
            print(f"Passed: {passed_count}")
            print(f"Failed: {failed_count}")
            print(f"Mean score: {mean_marks:.2f}")
            print(f"Lowest score: {lowest_marks}")
            print(f"Highest score: {highest_marks}")

            return results

        except Exception as e:
            print(f"Error calculating analytics: {e}")
            return None

def main():
    """Main function to run the student management system."""
    file_path = 'students.csv'
    try:
        manager = StudentManager(file_path)
        if manager.students is None and not os.path.exists(file_path):
            print("Failed to initialize student data. Exiting.")
            return
        
        while True:
            print("\nMenu:")
            print("1. Add student")
            print("2. Update student")
            print("3. Delete student")
            print("4. Show analytics")
            print("5. Exit")
            try:
                choice = input("Enter choice: ").strip()
                if choice == '1':
                    manager.add_student()
                elif choice == '2':
                    manager.update_student()
                elif choice == '3':
                    manager.delete_student()
                elif choice == '4':
                    manager.show_analytics()
                elif choice == '5':
                    print("Exiting program.")
                    break
                else:
                    print("Invalid choice. Please enter 1-5.")
            except KeyboardInterrupt:
                print("\nProgram interrupted. Exiting.")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
    except Exception as e:
        print(f"Error initializing program: {e}")

if __name__ == "__main__":
    main()
