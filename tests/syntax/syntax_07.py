# Задание: система управления студентами

class Student:
    def __init__(self, name, grades):
        self.name = name
        self.grades = grades

    def average(self):
        return sum(self.grades) / len(self.grades)

    def __repr__(self):
        return f"Student({self.name}, avg={self.average():.1f})"


class Group:
    def __init__(self, name):
        self.name = name
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def top_students(self, threshold=4.5):
        return [s for s in self.students if s.average() >= threshold]

    def failing_students(self, threshold=3.0):
        return [s for s in self.students if s.average() < threshold]

    def grade_distribution(self):
        distribution = {}
        for student in self.students:
            avg = round(student.average())
            if avg in distribution:
                distribution[avg] += 1
            else:
                distribution[avg] = 1
        return distribution

    def summary(self):
        averages = [s.average() for s in self.students]
        return {
            "total": len(self.students),
            "group_avg": sum(averages) / len(averages),
            "top": len(self.top_students()),
            "failing": len(self.failing_students())
        }


group = Group("2381")
students_data = [
    ("Анна", [5, 4, 5, 5, 4]),
    ("Борис", [3, 2, 3, 3, 2]),
    ("Виктор", [4, 4, 5, 4, 5]),
    ("Галина", [2, 3, 2, 3, 2]),
    ("Дмитрий", [5, 5, 5, 4, 5]),
]

for name, grades in students_data:
    group.add_student(Student(name, grades))

summary = group.summary()
print(f"Группа: {group.name}")
print(f"Студентов: {summary['total']}")
print(f"Средний балл: {summary['group_avg:.2f']}")
print(f"Отличников: {summary['top']}")
