import json
import csv
import os
from collections import defaultdict


class StudentGradeAnalyzer:
    def __init__(self):
        self.grade_scale = {
            'A': (90, 100),
            'B': (80, 89),
            'C': (70, 79),
            'D': (60, 69),
            'F': (0, 59)
        }
        self.students = []

    def add_student(self, name, score):
        """Add a student to the records"""
        if 0 <= score <= 100:
            self.students.append({'name': name, 'score': score})
            return True
        return False

    def get_letter_grade(self, score):
        """Convert numeric score to letter grade"""
        for grade, (low, high) in self.grade_scale.items():
            if low <= score <= high:
                return grade
        return 'F'

    def analyze_grades(self):
        """Analyze and display grade distribution"""
        if not self.students:
            print("No student data available.")
            return

        # Count grades
        grade_counts = defaultdict(int)
        for student in self.students:
            grade = self.get_letter_grade(student['score'])
            grade_counts[grade] += 1

        # Display results
        print("\n" + "=" * 50)
        print("GRADE ANALYSIS REPORT")
        print("=" * 50)

        print("\nGrade Distribution Table:")
        print("-" * 40)
        print(f"{'Grade':<10} {'Count':<10} {'Percentage':<10} {'Histogram':<10}")
        print("-" * 40)

        total_students = len(self.students)
        for grade in sorted(self.grade_scale.keys()):
            count = grade_counts[grade]
            percentage = (count / total_students) * 100 if total_students > 0 else 0
            histogram = "■" * int(count / max(grade_counts.values(), default=1) * 20)
            print(f"{grade:<10} {count:<10} {percentage:<10.1f}% {histogram}")

        # Statistics
        print("\nStatistics:")
        print("-" * 40)
        scores = [s['score'] for s in self.students]
        print(f"Total Students: {total_students}")
        print(f"Highest Score: {max(scores)}")
        print(f"Lowest Score: {min(scores)}")
        print(f"Average Score: {sum(scores) / total_students:.1f}")
        print(f"Passing Rate (A-D): {100 - grade_counts['F'] / total_students * 100:.1f}%")

        # Display individual student grades
        print("\nIndividual Student Grades:")
        print("-" * 40)
        print(f"{'Name':<15} {'Score':<10} {'Grade':<10}")
        print("-" * 40)
        for student in sorted(self.students, key=lambda x: x['score'], reverse=True):
            grade = self.get_letter_grade(student['score'])
            print(f"{student['name']:<15} {student['score']:<10} {grade:<10}")

    def save_to_file(self, filename="grades_report.txt"):
        """Save report to a file"""
        try:
            with open(filename, 'w') as f:
                f.write("GRADE ANALYSIS REPORT\n")
                f.write("=" * 50 + "\n\n")

                grade_counts = defaultdict(int)
                for student in self.students:
                    grade = self.get_letter_grade(student['score'])
                    grade_counts[grade] += 1

                f.write("Grade Distribution:\n")
                f.write("-" * 30 + "\n")
                total_students = len(self.students)
                for grade in sorted(self.grade_scale.keys()):
                    count = grade_counts[grade]
                    percentage = (count / total_students) * 100
                    f.write(f"Grade {grade}: {count} students ({percentage:.1f}%)\n")

                f.write("\nIndividual Student Records:\n")
                f.write("-" * 30 + "\n")
                for student in sorted(self.students, key=lambda x: x['score'], reverse=True):
                    grade = self.get_letter_grade(student['score'])
                    f.write(f"{student['name']}: {student['score']} (Grade: {grade})\n")

                f.write("\nStatistics:\n")
                f.write("-" * 30 + "\n")
                scores = [s['score'] for s in self.students]
                f.write(f"Total Students: {total_students}\n")
                f.write(f"Highest Score: {max(scores)}\n")
                f.write(f"Lowest Score: {min(scores)}\n")
                f.write(f"Average Score: {sum(scores) / total_students:.1f}\n")
                f.write(f"Passing Rate (A-D): {100 - grade_counts['F'] / total_students * 100:.1f}%\n")

            print(f"✓ Report saved to '{filename}'")
            return True
        except Exception as e:
            print(f"✗ Error saving file: {e}")
            return False

    def display_file_data(self, filename):
        """Display data from a saved file"""
        try:
            if not os.path.exists(filename):
                print(f"✗ File '{filename}' not found.")
                return False

            print(f"\n" + "=" * 50)
            print(f"CONTENTS OF FILE: {filename}")
            print("=" * 50)

            with open(filename, 'r') as f:
                content = f.read()
                print(content)

            # Show file info
            file_size = os.path.getsize(filename)
            print(f"\nFile Information:")
            print(f"Size: {file_size} bytes")

            return True
        except Exception as e:
            print(f"✗ Error reading file: {e}")
            return False

    def list_saved_files(self):
        """List all saved grade files in current directory"""
        print("\n" + "=" * 50)
        print("AVAILABLE SAVED FILES")
        print("=" * 50)

        # Look for grade-related files
        grade_files = []
        for file in os.listdir('.'):
            if file.endswith(('.txt', '.csv')) and ('grade' in file.lower() or 'report' in file.lower()):
                grade_files.append(file)

        if not grade_files:
            print("No grade files found in current directory.")
            return

        print("\nGrade Report Files:")
        for file in sorted(grade_files):
            size = os.path.getsize(file)
            print(f"  • {file} ({size} bytes)")

    def interactive_mode(self):
        """Interactive mode for entering student data"""
        print("\n" + "=" * 50)
        print("ENTER STUDENT DATA")
        print("=" * 50)
        print("\nEnter student data (type 'done' for name to finish):")

        while True:
            name = input("\nStudent name (or 'done' to finish): ").strip()
            if name.lower() == 'done':
                break

            try:
                score = float(input(f"Enter score for {name} (0-100): "))
                if self.add_student(name, score):
                    print(f"✓ Added {name} with score {score}")
                else:
                    print("✗ Invalid score! Must be between 0 and 100.")
            except ValueError:
                print("✗ Invalid input! Please enter a number.")

        if self.students:
            print(f"\n✓ Successfully entered data for {len(self.students)} students.")
            self.analyze_grades()

            save = input("\nSave report to file? (yes/no): ").lower()
            if save == 'yes':
                filename = input("Enter filename (default: 'grades_report.txt'): ").strip()
                if not filename:
                    filename = "grades_report.txt"
                self.save_to_file(filename)
                print(f"✓ Report saved to '{filename}'")
        else:
            print("\n✗ No student data entered.")


def main_menu():
    """Main menu for the program with 3 options"""
    analyzer = StudentGradeAnalyzer()

    while True:
        print("\n" + "=" * 50)
        print("STUDENT GRADE ANALYZER")
        print("=" * 50)
        print("\nOptions:")
        print("1. Enter and analyze student grades")
        print("2. Display data from saved file")
        print("3. Exit program")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            analyzer.interactive_mode()

        elif choice == "2":
            print("\nOptions for viewing files:")
            print("1. List available grade files")
            print("2. View specific file")

            view_choice = input("\nEnter choice (1 or 2): ").strip()

            if view_choice == "1":
                analyzer.list_saved_files()
            elif view_choice == "2":
                filename = input("Enter filename to display (e.g., 'grades_report.txt'): ").strip()
                if filename:
                    analyzer.display_file_data(filename)
                else:
                    print("✗ Please enter a filename.")
            else:
                print("✗ Invalid choice.")

        elif choice == "3":
            print("\n" + "=" * 50)
            print("Thank you for using Student Grade Analyzer!")
            print("=" * 50)
            break

        else:
            print("✗ Invalid choice. Please enter 1, 2, or 3.")

        # Pause before showing menu again
        if choice != "3":
            input("\nPress Enter to continue...")


# Main program
if __name__ == "__main__":
    main_menu()