class Student:
    count = 0

    def __init__(self, name, age):
        self._name = name
        self._age = age
        Student.count += 1

    def get_name(self) -> str:
        return self._name

    def get_age(self) -> int:
        return self._age

    def set_age(self, age: int) -> int:
        if age > self._age:
            self._age = age
        else:
            raise ValueError("Age can not be decreased")

    def bio(self):
        print(f"{self._name}, {self._age}")


def test_students():
    ruslan = Student("Ruslan", 18)
    ruslan.bio()
    ruslan.set_age(20)
    ruslan.bio()


test_students()
