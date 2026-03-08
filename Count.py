# Let us  do some coding for certain school grades

def count_students_by_grade():
    # Define grade ranges
    grade_ranges = {
        'A': (90, 100),
        'B': (80, 89),
        'C': (70, 79),
        'D': (60, 69),
        'F': (0, 59)
    }

    # Initializing counters
    counts = {grade: 0 for grade in grade_ranges}

    # Getting  student data
    num_students = int(input("Enter the number of students: "))

    for i in range(num_students):
        while True:
            try:
                score = float(input(f"Enter score for student {i + 1}: "))
                if 0 <= score <= 100:
                    # Determining  grade category
                    for grade, (low, high) in grade_ranges.items():
                        if low <= score <= high:
                            counts[grade] += 1
                            break
                    break
                else:
                    print("Score must be between 0 and 100. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    # Displaying  results
   # print("\n" + "=" * 40)
    print("GRADE DISTRIBUTION")
    #print("=" * 40)

    total_students = sum(counts.values())
    for grade, count in counts.items():
        percentage = (count / total_students * 100) if total_students > 0 else 0
        print(f"Grade {grade}: {count} students ({percentage:.1f}%)")


# Run the program
if __name__ == "__main__":
    count_students_by_grade()