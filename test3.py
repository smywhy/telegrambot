class Human:
    genom_count = 46

    def __init__(self, name: str, status:str = " "):
        self.name = name
        self.status = '10 lvl faceit'

    def description(self, ):
        return f'{self.status}{self.name}'

    def say(self, msg:str):
        return f'{self.status}{self.name}'

    @classmethod
    def change_genom_count(cls):
        cls.genom_count += 1

    @staticmethod
    def create_new_name():
        return choice(("smywhy", "triple"))


me = Human(name="smy",  status="10 lvl faceit")
print(me.create_new_name())









    @classmethod
    def change_years_old(cls):
        cls.years_old += 1

    @staticmethod
    def create_new_name():
        return choice("ilya", "Artem", "Nikita")


me = Student(name="Lev")
Student.change_years_old()
