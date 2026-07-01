class DatabaseConnection:
    def __enter__(self):
        print("Connecting to database...")

        self.connection = {
            "status": "connected"
        }

        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        print("Disconnecting from database...")

        if exc_type:
            print("An error occurred:", exc_value)

        return False


class ValidatedNumber:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Value must be a number")

        if value < self.min_value or value > self.max_value:
            raise ValueError(
                f"Value must be between {self.min_value} and {self.max_value}"
            )

        setattr(instance, self.private_name, value)


class Student:
    marks = ValidatedNumber(0, 100)

    def __init__(self, marks):
        self.marks = marks


print("Testing Database Connection")

with DatabaseConnection() as db:
    print("Database Status:", db["status"])

print("\n" + "-" * 40)

print("Testing Exception Handling")

try:
    with DatabaseConnection():
        print("Performing operation...")
        raise ValueError("Sample database error")
except ValueError as e:
    print("Caught Exception:", e)

print("\n" + "-" * 40)

print("Testing Descriptor")

student = Student(85)
print("Student Marks:", student.marks)

try:
    student.marks = 120
except ValueError as e:
    print("Validation Error:", e)