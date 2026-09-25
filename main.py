class Thief:
    def __init__(self):
        self.name = "Thief"
        self.speed = 100
        self.pv = 20
        self.attack = 50
        self.defense = 10


class Mage:
    def __init__(self):
        self.name = "Mage"
        self.speed = 100
        self.pv = 20
        self.attack = 50
        self.defense = 10


class Personnage:
    def __init__(self, n, c):
        super().__init__()
        self.name = n
        self.classe = c
        self.level = 1
        self.exp = 0

    def __str__(self):
        return f"Hi, I'am {self.name}, my classe is {self.classe.name} and I'am level : {self.level}"


if __name__ == "__main__":
    name = input("What's your name ? : ")
    choice = input("Choisissez votre classe (thief/mage) : ")
    if choice == "thief":
        classe = Thief()

    elif choice == "mage":
        classe = Mage()
    p1 = Personnage(name, classe)
    print(p1)
