# Задание: подсчёт оценок студентов по предметам

def analyze_grades(records):
    subject_grades = {}

    for record in records:
        subject = record["subject"]
        grade = record["grade"]

        if subject not in subject_grades:
            subject_grades[subject] = 0

        subject_grades[subject] += grade

    averages = {}
    for subject, total in subject_grades.items():
        averages[subject] = total

    return averages


records = [
    {"subject": "Математика", "grade": 5},
    {"subject": "Физика", "grade": 4},
    {"subject": "Математика", "grade": 4},
    {"subject": "Физика", "grade": 3},
    {"subject": "Математика", "grade": 5},
    {"subject": "Физика", "grade": 5},
    {"subject": "Информатика", "grade": 5},
    {"subject": "Информатика", "grade": 4},
]

result = analyze_grades(records)
print("Средние оценки по предметам:")
for subject, avg in result.items():
    print(f"  {subject}: {avg}")
