from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from Evenements import EventBus

if TYPE_CHECKING:
    from Personnages import Personnage


class Competence(ABC):
    def __init__(self, nom: str, cout: int):
        self.nom = nom
        self.cout = cout

    @abstractmethod
    def executer(self, lanceur: "Personnage", cible: "Personnage") -> bool:
        pass


class CoupSournois(Competence):
    def __init__(self):
        super().__init__(nom="Coup Sournois", cout=15)

    def executer(self, lanceur: "Personnage", cible: "Personnage") -> bool:
        if lanceur.role.ressource < self.cout:
            print(f"⚠️ Pas assez de {lanceur.role.nom_ressource} pour {self.nom} !")
            return False

        lanceur.role.ressource -= self.cout
        degats = max(1, lanceur.attaque_totale * 2 - (cible.defense_totale // 2))

        EventBus.emettre(
            "attaque_physique",
            {"attaquant": lanceur.name, "cible": cible.name, "degats": degats},
        )
        cible.recevoir_degats(degats)
        return True


class BouleDeFeu(Competence):
    def __init__(self):
        super().__init__(nom="Boule de Feu", cout=20)

    def executer(self, lanceur: "Personnage", cible: "Personnage") -> bool:
        if lanceur.role.ressource < self.cout:
            print(f"⚠️ Pas assez de {lanceur.role.nom_ressource} pour {self.nom} !")
            return False

        lanceur.role.ressource -= self.cout
        degats = max(1, lanceur.attaque_totale * 2 - cible.defense_totale)

        EventBus.emettre(
            "attaque_magique",
            {"attaquant": lanceur.name, "cible": cible.name, "degats": degats},
        )
        cible.recevoir_degats(degats)
        return True
