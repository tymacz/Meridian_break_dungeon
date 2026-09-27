from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from Competences import Competence, CoupSournois, BouleDeFeu
from Evenements import EventBus

if TYPE_CHECKING:
    from Personnages import Personnage

class Role(ABC):
    def __init__(self, name: str, speed: int, pv: int, attack: int, defense: int, nom_ressource: str, ressource_max: int):
        self.name = name
        self.speed = speed
        self.pv = pv
        self.attack = attack
        self.defense = defense
        self.nom_ressource = nom_ressource
        self.ressource_max = ressource_max
        self.ressource = ressource_max
        self.competences :  list['Competence'] = []

    @abstractmethod
    def offensive_action(self, attaquant: "Personnage", cible: "Personnage"):
        pass

    def to_dict(self) -> dict:
        """Convertit le rôle en dictionnaire pour la sérialisation."""
        return {
            "speed": self.speed,
            "pv": self.pv,
            "attack": self.attack,
            "defense": self.defense,
            "type": self.__class__.__name__,
        }

    def regenerer_ressource(self, montant: int = 5):
        self.ressource = min(self.ressource_max, self.ressource + montant)


class Thief(Role):
    def __init__(self):
        super().__init__(name="Thief", speed=120, pv=20, attack=40, defense=10, nom_ressource="Energie", ressource_max=50)
        self.competences.append(CoupSournois())
    def offensive_action(self, attaquant: "Personnage", cible: "Personnage"):
        degats = max(1, attaquant.attaque_totale - (cible.defense_totale // 2))
        EventBus.emettre("attaque_physique", {
                    "attaquant": attaquant.name,
                    "cible": cible.name,
                    "degats": degats
                })
        cible.recevoir_degats(degats)


class Mage(Role):
    def __init__(self):
        super().__init__(name="Mage", speed=100, pv=15, attack=60, defense=5, nom_ressource="Mana", ressource_max=80)
        self.competences.append(BouleDeFeu())
        
    def offensive_action(self, attaquant: "Personnage", cible: "Personnage"):
        degats = max(1, attaquant.attaque_totale - cible.defense_totale)
        EventBus.emettre("attaque_magique", {
                    "attaquant": attaquant.name,
                    "cible": cible.name,
                    "degats": degats
                })
        cible.recevoir_degats(degats)
