from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Personnages import Personnage

class Role(ABC):
    def __init__(self, name: str, speed: int, pv: int, attack: int, defense: int):
        self.name = name
        self.speed = speed
        self.pv = pv
        self.attack = attack
        self.defense = defense

    @abstractmethod
    def offensive_action(self, attaquant: "Personnage", cible: "Personnage"):
        pass


class Thief(Role):
    def __init__(self):
        super().__init__(name="Thief", speed=120, pv=20, attack=40, defense=10)

    def offensive_action(self, attaquant: "Personnage", cible: "Personnage"):
        degats = max(1, attaquant.attaque_totale - (cible.role.defense // 2))
        print(
            f"🗡️ {attaquant.name} poignarde sournoisement {cible.name} pour {degats} dégâts !"
        )
        cible.recevoir_degats(degats)


class Mage(Role):
    def __init__(self):
        super().__init__(name="Mage", speed=100, pv=15, attack=60, defense=5)

    def offensive_action(self, attaquant: "Personnage", cible: "Personnage"):
        degats = max(1, attaquant.attaque_totale - cible.role.defense)
        print(
            f"🔥 {attaquant.name} lance une boule de feu sur {cible.name} pour {degats} dégâts !"
        )
        cible.recevoir_degats(degats)
